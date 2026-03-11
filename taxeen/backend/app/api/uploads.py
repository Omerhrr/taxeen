"""
Statement Uploads API Routes
Upload and parse bank statement PDFs
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
import hashlib
import json

from app.database import get_db
from app.models import User, BankAccount, StatementUpload, Transaction
from app.auth import get_current_user
from app.config import settings, ensure_upload_dir
from app.schemas.statement import (
    StatementUploadResponse,
    StatementList,
    StatementDetail,
    StatementVerifyRequest,
    ParseResult,
)
from app.schemas.common import MessageResponse, PaginationParams

router = APIRouter(prefix="/uploads", tags=["Statement Uploads"])


def calculate_file_hash(file_content: bytes) -> str:
    """Calculate SHA-256 hash of file content"""
    return hashlib.sha256(file_content).hexdigest()


async def process_statement_background(
    upload_id: int,
    file_path: str,
    db_url: str = settings.DATABASE_URL
):
    """
    Background task to process uploaded statement
    """
    from app.database import SessionLocal
    from app.parsers.statement_parser import StatementParser
    from app.utils.transfer_detector import TransferDetector
    
    db = SessionLocal()
    try:
        upload = db.query(StatementUpload).filter(StatementUpload.id == upload_id).first()
        if not upload:
            return
        
        # Update status
        upload.status = "processing"
        upload.processing_started = datetime.utcnow()
        db.commit()
        
        # Parse the statement
        parser = StatementParser()
        result = parser.parse(file_path)
        
        if result.success:
            # Save transactions
            bank_account_id = upload.bank_account_id
            user_id = upload.user_id
            
            for tx_data in result.transactions:
                transaction = Transaction(
                    user_id=user_id,
                    bank_account_id=bank_account_id,
                    statement_upload_id=upload_id,
                    transaction_date=tx_data.date,
                    value_date=tx_data.value_date,
                    transaction_type=tx_data.transaction_type,
                    amount=tx_data.amount,
                    balance=tx_data.balance,
                    description=tx_data.description,
                    reference=tx_data.reference,
                )
                db.add(transaction)
            
            # Update upload record
            upload.total_transactions = result.total_transactions
            upload.total_credits = result.total_credits
            upload.total_debits = result.total_debits
            upload.opening_balance = result.opening_balance
            upload.closing_balance = result.closing_balance
            upload.statement_start_date = result.statement_start_date
            upload.statement_end_date = result.statement_end_date
            upload.extraction_method = result.extraction_method
            upload.status = "completed"
            upload.processing_completed = datetime.utcnow()
            
            if result.errors:
                upload.parsing_errors = json.dumps(result.errors)
            if result.warnings:
                upload.warnings = json.dumps(result.warnings)
            
            db.commit()
            
            # Run internal transfer detection
            detector = TransferDetector(db)
            detector.detect_for_user(user_id)
            
        else:
            upload.status = "failed"
            upload.parsing_errors = json.dumps(result.errors)
            upload.processing_completed = datetime.utcnow()
            db.commit()
            
    except Exception as e:
        upload.status = "failed"
        upload.parsing_errors = json.dumps([str(e)])
        upload.processing_completed = datetime.utcnow()
        db.commit()
    finally:
        db.close()


@router.post("", response_model=StatementUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_statement(
    background_tasks: BackgroundTasks,
    bank_account_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a bank statement PDF
    
    - Validates file type and size
    - Stores file securely
    - Processes in background
    """
    # Validate bank account belongs to user
    bank_account = db.query(BankAccount).filter(
        BankAccount.id == bank_account_id,
        BankAccount.user_id == current_user.id
    ).first()
    
    if not bank_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank account not found"
        )
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are accepted"
        )
    
    # Read file content
    content = await file.read()
    
    # Validate file size
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    # Ensure upload directory exists
    ensure_upload_dir()
    
    # Calculate file hash for deduplication
    file_hash = calculate_file_hash(content)
    
    # Check for duplicate
    existing = db.query(StatementUpload).filter(
        StatementUpload.user_id == current_user.id,
        StatementUpload.file_hash == file_hash
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This statement has already been uploaded"
        )
    
    # Save file
    upload_dir = os.path.join(settings.UPLOAD_DIR, "statements", str(current_user.id))
    os.makedirs(upload_dir, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    file_name = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, file_name)
    
    with open(file_path, 'wb') as f:
        f.write(content)
    
    # Create upload record
    upload = StatementUpload(
        user_id=current_user.id,
        bank_account_id=bank_account_id,
        file_name=file.filename,
        file_path=file_path,
        file_size=len(content),
        file_hash=file_hash,
        status="pending",
    )
    
    db.add(upload)
    db.commit()
    db.refresh(upload)
    
    # Process in background
    background_tasks.add_task(
        process_statement_background,
        upload.id,
        file_path
    )
    
    return StatementUploadResponse.from_orm(upload)


@router.get("", response_model=StatementList)
async def list_uploads(
    bank_account_id: Optional[int] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List statement uploads
    """
    query = db.query(StatementUpload).filter(
        StatementUpload.user_id == current_user.id
    )
    
    if bank_account_id:
        query = query.filter(StatementUpload.bank_account_id == bank_account_id)
    
    if status_filter:
        query = query.filter(StatementUpload.status == status_filter)
    
    total = query.count()
    
    offset = (page - 1) * per_page
    uploads = query.order_by(
        StatementUpload.created_at.desc()
    ).offset(offset).limit(per_page).all()
    
    pages = (total + per_page - 1) // per_page
    
    return StatementList(
        items=[StatementUploadResponse.from_orm(u) for u in uploads],
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
    )


@router.get("/{upload_id}", response_model=StatementDetail)
async def get_upload(
    upload_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get details of a specific upload
    """
    upload = db.query(StatementUpload).filter(
        StatementUpload.id == upload_id,
        StatementUpload.user_id == current_user.id
    ).first()
    
    if not upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upload not found"
        )
    
    response = StatementDetail.from_orm(upload)
    
    # Parse errors and warnings
    if upload.parsing_errors:
        try:
            response.parsing_errors = json.loads(upload.parsing_errors)
        except:
            pass
    
    if upload.warnings:
        try:
            response.warnings = json.loads(upload.warnings)
        except:
            pass
    
    return response


@router.post("/{upload_id}/verify", response_model=MessageResponse)
async def verify_upload(
    upload_id: int,
    verify_data: StatementVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify an uploaded statement
    """
    upload = db.query(StatementUpload).filter(
        StatementUpload.id == upload_id,
        StatementUpload.user_id == current_user.id
    ).first()
    
    if not upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upload not found"
        )
    
    upload.is_verified = verify_data.verified
    upload.verification_notes = verify_data.notes
    upload.verified_by = current_user.id
    upload.verification_date = datetime.utcnow()
    
    db.commit()
    
    return MessageResponse(message="Statement verification updated")


@router.delete("/{upload_id}", response_model=MessageResponse)
async def delete_upload(
    upload_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an upload and its transactions
    """
    upload = db.query(StatementUpload).filter(
        StatementUpload.id == upload_id,
        StatementUpload.user_id == current_user.id
    ).first()
    
    if not upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upload not found"
        )
    
    # Delete file
    if upload.file_path and os.path.exists(upload.file_path):
        os.remove(upload.file_path)
    
    # Delete from database (cascade deletes transactions)
    db.delete(upload)
    db.commit()
    
    return MessageResponse(message="Upload deleted successfully")


@router.post("/{upload_id}/reprocess", response_model=MessageResponse)
async def reprocess_upload(
    upload_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Reprocess a previously uploaded statement
    """
    upload = db.query(StatementUpload).filter(
        StatementUpload.id == upload_id,
        StatementUpload.user_id == current_user.id
    ).first()
    
    if not upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upload not found"
        )
    
    if not upload.file_path or not os.path.exists(upload.file_path):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Original file not found"
        )
    
    # Delete existing transactions
    db.query(Transaction).filter(
        Transaction.statement_upload_id == upload_id
    ).delete()
    
    # Reset upload status
    upload.status = "pending"
    upload.total_transactions = 0
    upload.total_credits = 0
    upload.total_debits = 0
    upload.parsing_errors = None
    upload.warnings = None
    db.commit()
    
    # Reprocess in background
    background_tasks.add_task(
        process_statement_background,
        upload.id,
        upload.file_path
    )
    
    return MessageResponse(message="Statement queued for reprocessing")


@router.get("/{upload_id}/transactions")
async def get_upload_transactions(
    upload_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all transactions from a specific upload
    """
    upload = db.query(StatementUpload).filter(
        StatementUpload.id == upload_id,
        StatementUpload.user_id == current_user.id
    ).first()
    
    if not upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upload not found"
        )
    
    transactions = db.query(Transaction).filter(
        Transaction.statement_upload_id == upload_id
    ).order_by(Transaction.transaction_date).all()
    
    return {
        "upload_id": upload_id,
        "total": len(transactions),
        "transactions": [tx.to_dict() for tx in transactions]
    }
