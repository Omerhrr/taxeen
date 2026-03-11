"""
Transactions API Routes
List, filter, classify transactions
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from app.database import get_db
from app.models import User, BankAccount, Transaction
from app.auth import get_current_user
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionList,
    TransactionFilter,
    TransactionClassify,
    TransactionSummary,
    BulkClassifyRequest,
)
from app.schemas.common import MessageResponse, PaginationParams

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def apply_transaction_filters(query, filters: TransactionFilter):
    """Apply filters to transaction query"""
    if filters.bank_account_id:
        query = query.filter(Transaction.bank_account_id == filters.bank_account_id)
    
    if filters.date_from:
        query = query.filter(Transaction.transaction_date >= filters.date_from)
    
    if filters.date_to:
        query = query.filter(Transaction.transaction_date <= filters.date_to)
    
    if filters.transaction_type:
        query = query.filter(Transaction.transaction_type == filters.transaction_type)
    
    if filters.category:
        query = query.filter(Transaction.category == filters.category)
    
    if filters.min_amount is not None:
        query = query.filter(Transaction.amount >= filters.min_amount)
    
    if filters.max_amount is not None:
        query = query.filter(Transaction.amount <= filters.max_amount)
    
    if filters.is_taxable is not None:
        query = query.filter(Transaction.is_taxable == filters.is_taxable)
    
    if filters.is_deductible is not None:
        query = query.filter(Transaction.is_deductible == filters.is_deductible)
    
    if filters.is_internal_transfer is not None:
        query = query.filter(Transaction.is_internal_transfer == filters.is_internal_transfer)
    
    if filters.search:
        search_pattern = f"%{filters.search}%"
        query = query.filter(
            or_(
                Transaction.description.ilike(search_pattern),
                Transaction.counterparty_name.ilike(search_pattern),
                Transaction.reference.ilike(search_pattern),
            )
        )
    
    return query


@router.get("", response_model=TransactionList)
async def list_transactions(
    bank_account_id: Optional[int] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    transaction_type: Optional[str] = None,
    category: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    is_taxable: Optional[bool] = None,
    is_deductible: Optional[bool] = None,
    is_internal_transfer: Optional[bool] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List transactions with optional filtering
    
    Supports pagination and multiple filter criteria
    """
    # Base query - only user's transactions
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)
    
    # Apply filters
    filters = TransactionFilter(
        bank_account_id=bank_account_id,
        date_from=date_from,
        date_to=date_to,
        transaction_type=transaction_type,
        category=category,
        min_amount=min_amount,
        max_amount=max_amount,
        is_taxable=is_taxable,
        is_deductible=is_deductible,
        is_internal_transfer=is_internal_transfer,
        search=search,
    )
    query = apply_transaction_filters(query, filters)
    
    # Get total count
    total = query.count()
    
    # Calculate totals
    total_credits = query.filter(
        Transaction.transaction_type.in_(["credit", "transfer_in"]),
        Transaction.is_internal_transfer == False
    ).with_entities(func.sum(Transaction.amount)).scalar() or 0
    
    total_debits = query.filter(
        Transaction.transaction_type.in_(["debit", "transfer_out"]),
        Transaction.is_internal_transfer == False
    ).with_entities(func.sum(Transaction.amount)).scalar() or 0
    
    # Apply pagination
    offset = (page - 1) * per_page
    transactions = query.order_by(
        Transaction.transaction_date.desc()
    ).offset(offset).limit(per_page).all()
    
    # Calculate pages
    pages = (total + per_page - 1) // per_page
    
    return TransactionList(
        items=[TransactionResponse.from_orm(tx) for tx in transactions],
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
        total_credits=total_credits,
        total_debits=total_debits,
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get details of a specific transaction
    """
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return TransactionResponse.from_orm(transaction)


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    update_data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update transaction details (category, notes, tax info)
    """
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Update fields
    if update_data.category is not None:
        transaction.category = update_data.category
    
    if update_data.sub_category is not None:
        transaction.sub_category = update_data.sub_category
    
    if update_data.is_taxable is not None:
        transaction.is_taxable = update_data.is_taxable
    
    if update_data.is_deductible is not None:
        transaction.is_deductible = update_data.is_deductible
    
    if update_data.tax_category is not None:
        transaction.tax_category = update_data.tax_category
    
    if update_data.user_notes is not None:
        transaction.user_notes = update_data.user_notes
    
    if update_data.user_tags is not None:
        transaction.user_tags = update_data.user_tags
    
    db.commit()
    db.refresh(transaction)
    
    return TransactionResponse.from_orm(transaction)


@router.post("/{transaction_id}/classify", response_model=TransactionResponse)
async def classify_transaction(
    transaction_id: int,
    classification: TransactionClassify,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Classify a transaction for tax purposes
    """
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Apply classification
    transaction.category = classification.category
    transaction.sub_category = classification.sub_category
    transaction.is_taxable = classification.is_taxable
    transaction.is_deductible = classification.is_deductible
    transaction.tax_category = classification.tax_category
    
    db.commit()
    db.refresh(transaction)
    
    return TransactionResponse.from_orm(transaction)


@router.post("/bulk-classify", response_model=MessageResponse)
async def bulk_classify_transactions(
    request: BulkClassifyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Classify multiple transactions at once
    """
    # Verify all transactions belong to user
    transactions = db.query(Transaction).filter(
        Transaction.id.in_(request.transaction_ids),
        Transaction.user_id == current_user.id
    ).all()
    
    if len(transactions) != len(request.transaction_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Some transactions not found or don't belong to you"
        )
    
    # Update all transactions
    for transaction in transactions:
        transaction.category = request.classification.category
        transaction.sub_category = request.classification.sub_category
        transaction.is_taxable = request.classification.is_taxable
        transaction.is_deductible = request.classification.is_deductible
        transaction.tax_category = request.classification.tax_category
    
    db.commit()
    
    return MessageResponse(
        message=f"Successfully classified {len(transactions)} transactions"
    )


@router.delete("/{transaction_id}", response_model=MessageResponse)
async def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a transaction
    """
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    db.delete(transaction)
    db.commit()
    
    return MessageResponse(message="Transaction deleted")


@router.get("/summary/overview", response_model=TransactionSummary)
async def get_transaction_summary(
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    bank_account_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get transaction summary statistics
    """
    # Base query
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)
    
    if bank_account_id:
        query = query.filter(Transaction.bank_account_id == bank_account_id)
    
    if date_from:
        query = query.filter(Transaction.transaction_date >= date_from)
    
    if date_to:
        query = query.filter(Transaction.transaction_date <= date_to)
    
    # Get all transactions for summary
    transactions = query.all()
    
    # Calculate statistics
    total_transactions = len(transactions)
    total_credits = sum(tx.amount for tx in transactions if tx.is_income and not tx.is_internal_transfer)
    total_debits = sum(tx.amount for tx in transactions if tx.is_expense and not tx.is_internal_transfer)
    net_flow = total_credits - total_debits
    
    # Group by category
    by_category = {}
    for tx in transactions:
        if not tx.is_internal_transfer:
            if tx.category not in by_category:
                by_category[tx.category] = {"count": 0, "amount": 0.0}
            by_category[tx.category]["count"] += 1
            by_category[tx.category]["amount"] += tx.amount
    
    # Group by month
    by_month = {}
    for tx in transactions:
        month_key = tx.transaction_date.strftime("%Y-%m")
        if month_key not in by_month:
            by_month[month_key] = {"credits": 0.0, "debits": 0.0}
        if tx.is_income and not tx.is_internal_transfer:
            by_month[month_key]["credits"] += tx.amount
        elif tx.is_expense and not tx.is_internal_transfer:
            by_month[month_key]["debits"] += tx.amount
    
    # Tax calculations
    taxable_income = sum(tx.amount for tx in transactions if tx.is_taxable and tx.is_income and not tx.is_internal_transfer)
    deductible_expenses = sum(tx.amount for tx in transactions if tx.is_deductible and tx.is_expense)
    internal_transfers = sum(1 for tx in transactions if tx.is_internal_transfer)
    
    return TransactionSummary(
        total_transactions=total_transactions,
        total_credits=total_credits,
        total_debits=total_debits,
        net_flow=net_flow,
        by_category=by_category,
        by_month=by_month,
        taxable_income=taxable_income,
        deductible_expenses=deductible_expenses,
        internal_transfers=internal_transfers,
    )


@router.get("/categories/list")
async def list_categories():
    """
    Get list of transaction categories
    """
    from app.schemas.transaction import TransactionCategory
    
    income_categories = [
        {"value": cat.value, "label": cat.value.replace("_", " ").title()}
        for cat in TransactionCategory
        if cat.value in ["salary", "business_income", "investment", "rental_income", "other_income"]
    ]
    
    expense_categories = [
        {"value": cat.value, "label": cat.value.replace("_", " ").title()}
        for cat in TransactionCategory
        if cat.value not in ["salary", "business_income", "investment", "rental_income", "other_income", "uncategorized"]
    ]
    
    return {
        "income": income_categories,
        "expense": expense_categories,
        "all": [{"value": cat.value, "label": cat.value.replace("_", " ").title()} for cat in TransactionCategory]
    }


@router.post("/{transaction_id}/mark-internal-transfer")
async def mark_internal_transfer(
    transaction_id: int,
    related_transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Manually mark a transaction as internal transfer
    """
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()
    
    related = db.query(Transaction).filter(
        Transaction.id == related_transaction_id,
        Transaction.user_id == current_user.id
    ).first()
    
    if not transaction or not related:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Mark both as internal transfers
    transaction.is_internal_transfer = True
    transaction.is_taxable = False
    transaction.related_transaction_id = related.id
    transaction.related_bank_account_id = related.bank_account_id
    
    related.is_internal_transfer = True
    related.is_taxable = False
    related.related_transaction_id = transaction.id
    related.related_bank_account_id = transaction.bank_account_id
    
    db.commit()
    
    return {"message": "Transactions marked as internal transfer", "transaction_ids": [transaction_id, related_transaction_id]}
