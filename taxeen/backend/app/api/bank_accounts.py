"""
Bank Accounts API Routes
CRUD operations for user bank accounts
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models import User, BankAccount, Transaction
from app.auth import get_current_user
from app.schemas.bank_account import (
    BankAccountCreate,
    BankAccountUpdate,
    BankAccountResponse,
    BankAccountList,
    BankAccountDetail,
)
from app.schemas.common import MessageResponse, PaginationParams
from app.models.bank_account import NIGERIAN_BANK_CODES

router = APIRouter(prefix="/bank-accounts", tags=["Bank Accounts"])


@router.post("", response_model=BankAccountResponse, status_code=status.HTTP_201_CREATED)
async def create_bank_account(
    account_data: BankAccountCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a new bank account for the user
    
    - Validates account number format
    - Sets bank name from code if provided
    - Returns created account with masked number
    """
    # Check if account already exists for this user
    existing = db.query(BankAccount).filter(
        BankAccount.user_id == current_user.id,
        BankAccount.account_number == account_data.account_number
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This bank account is already linked to your profile"
        )
    
    # Get bank name from code if provided
    bank_name = account_data.bank_name
    if account_data.bank_code:
        bank_name = NIGERIAN_BANK_CODES.get(account_data.bank_code, account_data.bank_name)
    
    # Create bank account
    bank_account = BankAccount(
        user_id=current_user.id,
        bank_name=bank_name,
        bank_code=account_data.bank_code,
        account_number=account_data.account_number,
        account_name=account_data.account_name,
        account_type=account_data.account_type,
        currency=account_data.currency,
        notes=account_data.notes,
        is_active=True,
        is_verified=False,
    )
    
    db.add(bank_account)
    db.commit()
    db.refresh(bank_account)
    
    # Get transactions count
    tx_count = db.query(Transaction).filter(
        Transaction.bank_account_id == bank_account.id
    ).count()
    
    return BankAccountResponse.from_orm(bank_account, tx_count)


@router.get("", response_model=BankAccountList)
async def list_bank_accounts(
    include_inactive: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all bank accounts for the current user
    
    - Returns accounts with masked numbers
    - Optionally includes inactive accounts
    """
    query = db.query(BankAccount).filter(BankAccount.user_id == current_user.id)
    
    if not include_inactive:
        query = query.filter(BankAccount.is_active == True)
    
    accounts = query.order_by(BankAccount.created_at.desc()).all()
    
    # Calculate totals and get transaction counts
    account_responses = []
    total_balance = 0.0
    
    for account in accounts:
        tx_count = db.query(Transaction).filter(
            Transaction.bank_account_id == account.id
        ).count()
        account_responses.append(BankAccountResponse.from_orm(account, tx_count))
        if account.is_active:
            total_balance += account.current_balance or 0.0
    
    return BankAccountList(
        accounts=account_responses,
        total=len(account_responses),
        total_balance=total_balance
    )


@router.get("/{account_id}", response_model=BankAccountDetail)
async def get_bank_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get details of a specific bank account
    """
    account = db.query(BankAccount).filter(
        BankAccount.id == account_id,
        BankAccount.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank account not found"
        )
    
    # Get recent transactions
    recent_transactions = db.query(Transaction).filter(
        Transaction.bank_account_id == account.id
    ).order_by(Transaction.transaction_date.desc()).limit(5).all()
    
    # Get statement uploads count
    from app.models import StatementUpload
    statement_count = db.query(StatementUpload).filter(
        StatementUpload.bank_account_id == account.id
    ).count()
    
    # Get last statement date
    last_statement = db.query(StatementUpload).filter(
        StatementUpload.bank_account_id == account.id
    ).order_by(StatementUpload.created_at.desc()).first()
    
    tx_count = db.query(Transaction).filter(
        Transaction.bank_account_id == account.id
    ).count()
    
    response = BankAccountDetail.from_orm(account, tx_count)
    response.recent_transactions = [tx.to_dict() for tx in recent_transactions]
    response.statement_uploads_count = statement_count
    response.last_statement_date = last_statement.created_at if last_statement else None
    
    return response


@router.put("/{account_id}", response_model=BankAccountResponse)
async def update_bank_account(
    account_id: int,
    update_data: BankAccountUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update bank account details
    """
    account = db.query(BankAccount).filter(
        BankAccount.id == account_id,
        BankAccount.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank account not found"
        )
    
    # Update fields
    if update_data.account_name is not None:
        account.account_name = update_data.account_name
    if update_data.account_type is not None:
        account.account_type = update_data.account_type
    if update_data.notes is not None:
        account.notes = update_data.notes
    if update_data.is_active is not None:
        account.is_active = update_data.is_active
    
    db.commit()
    db.refresh(account)
    
    tx_count = db.query(Transaction).filter(
        Transaction.bank_account_id == account.id
    ).count()
    
    return BankAccountResponse.from_orm(account, tx_count)


@router.delete("/{account_id}", response_model=MessageResponse)
async def delete_bank_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a bank account
    
    Note: This will cascade delete all related transactions and uploads
    """
    account = db.query(BankAccount).filter(
        BankAccount.id == account_id,
        BankAccount.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank account not found"
        )
    
    # Check for existing transactions
    tx_count = db.query(Transaction).filter(
        Transaction.bank_account_id == account.id
    ).count()
    
    if tx_count > 0:
        # Instead of deleting, deactivate
        account.is_active = False
        db.commit()
        return MessageResponse(
            message=f"Bank account deactivated. {tx_count} transactions preserved."
        )
    
    db.delete(account)
    db.commit()
    
    return MessageResponse(message="Bank account deleted successfully")


@router.post("/{account_id}/verify", response_model=MessageResponse)
async def verify_bank_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify bank account with CBN/NIBSS
    
    Note: In production, this would call Paystack or NIBSS API
    """
    account = db.query(BankAccount).filter(
        BankAccount.id == account_id,
        BankAccount.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank account not found"
        )
    
    # Mock verification - in production, call Paystack/NIBSS
    # For now, just mark as verified
    account.is_verified = True
    account.verification_status = "verified"
    db.commit()
    
    return MessageResponse(message="Bank account verified successfully")


@router.get("/{account_id}/balance")
async def get_account_balance(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current balance for a bank account
    """
    account = db.query(BankAccount).filter(
        BankAccount.id == account_id,
        BankAccount.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank account not found"
        )
    
    # Calculate balance from transactions
    credits = db.query(Transaction).filter(
        Transaction.bank_account_id == account.id,
        Transaction.transaction_type.in_(["credit", "transfer_in"]),
        Transaction.is_internal_transfer == False
    ).with_entities(Transaction.amount)
    
    debits = db.query(Transaction).filter(
        Transaction.bank_account_id == account.id,
        Transaction.transaction_type.in_(["debit", "transfer_out"]),
        Transaction.is_internal_transfer == False
    ).with_entities(Transaction.amount)
    
    total_credits = sum([t[0] for t in credits.all()]) if credits.count() > 0 else 0
    total_debits = sum([t[0] for t in debits.all()]) if debits.count() > 0 else 0
    calculated_balance = total_credits - total_debits
    
    return {
        "account_id": account.id,
        "bank_name": account.bank_name,
        "masked_number": account.masked_account_number,
        "current_balance": account.current_balance or calculated_balance,
        "calculated_balance": calculated_balance,
        "total_credits": total_credits,
        "total_debits": total_debits,
        "last_updated": account.last_sync.isoformat() if account.last_sync else None
    }


@router.get("/banks/list")
async def list_nigerian_banks():
    """
    Get list of Nigerian banks with codes
    """
    return {
        "banks": [
            {"code": code, "name": name}
            for code, name in sorted(NIGERIAN_BANK_CODES.items(), key=lambda x: x[1])
        ]
    }
