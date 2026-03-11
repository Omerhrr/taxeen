"""
Transaction Schemas
Request/Response models for transaction endpoints
"""

from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from enum import Enum


class TransactionType(str, Enum):
    """Transaction type enum"""
    CREDIT = "credit"
    DEBIT = "debit"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"


class TransactionCategory(str, Enum):
    """Transaction categories for tax purposes"""
    # Income categories
    SALARY = "salary"
    BUSINESS_INCOME = "business_income"
    INVESTMENT = "investment"
    RENTAL_INCOME = "rental_income"
    OTHER_INCOME = "other_income"
    
    # Expense categories
    FOOD = "food"
    TRANSPORT = "transport"
    UTILITIES = "utilities"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    RENT = "rent"
    INSURANCE = "insurance"
    TAX_PAYMENT = "tax_payment"
    LOAN_REPAYMENT = "loan_repayment"
    INVESTMENT_EXPENSE = "investment_expense"
    BUSINESS_EXPENSE = "business_expense"
    PENSION = "pension"
    NHF = "nhf"  # National Housing Fund
    NHIS = "nhis"  # National Health Insurance Scheme
    MORTGAGE_INTEREST = "mortgage_interest"
    CHARITABLE_DONATION = "charitable_donation"
    OTHER_EXPENSE = "other_expense"
    
    UNCATEGORIZED = "uncategorized"


class TransactionBase(BaseModel):
    """Base transaction schema"""
    transaction_date: datetime
    transaction_type: str = Field(..., pattern="^(credit|debit|transfer_in|transfer_out)$")
    amount: float = Field(..., gt=0)
    description: Optional[str] = None
    balance: Optional[float] = None


class TransactionCreate(TransactionBase):
    """Transaction creation schema"""
    bank_account_id: int
    value_date: Optional[datetime] = None
    reference: Optional[str] = Field(None, max_length=100)
    narration: Optional[str] = None
    counterparty_name: Optional[str] = Field(None, max_length=255)
    counterparty_account: Optional[str] = Field(None, max_length=50)
    counterparty_bank: Optional[str] = Field(None, max_length=100)
    category: str = Field(default="uncategorized")
    user_notes: Optional[str] = None


class TransactionUpdate(BaseModel):
    """Transaction update schema"""
    category: Optional[str] = None
    sub_category: Optional[str] = None
    is_taxable: Optional[bool] = None
    is_deductible: Optional[bool] = None
    tax_category: Optional[str] = None
    user_notes: Optional[str] = None
    user_tags: Optional[str] = None


class TransactionResponse(BaseModel):
    """Transaction response schema"""
    id: int
    bank_account_id: int
    transaction_date: datetime
    value_date: Optional[datetime] = None
    transaction_type: str
    amount: float
    formatted_amount: str
    balance: Optional[float] = None
    description: Optional[str] = None
    reference: Optional[str] = None
    counterparty_name: Optional[str] = None
    counterparty_bank: Optional[str] = None
    category: str
    sub_category: Optional[str] = None
    is_income: bool
    is_expense: bool
    is_internal_transfer: bool
    is_taxable: bool
    is_deductible: bool
    tax_category: Optional[str] = None
    user_notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_orm(cls, tx):
        """Create response from ORM model"""
        return cls(
            id=tx.id,
            bank_account_id=tx.bank_account_id,
            transaction_date=tx.transaction_date,
            value_date=tx.value_date,
            transaction_type=tx.transaction_type,
            amount=tx.amount,
            formatted_amount=f"₦{tx.amount:,.2f}",
            balance=tx.balance,
            description=tx.description,
            reference=tx.reference,
            counterparty_name=tx.counterparty_name,
            counterparty_bank=tx.counterparty_bank,
            category=tx.category,
            sub_category=tx.sub_category,
            is_income=tx.is_income,
            is_expense=tx.is_expense,
            is_internal_transfer=tx.is_internal_transfer,
            is_taxable=tx.is_taxable,
            is_deductible=tx.is_deductible,
            tax_category=tx.tax_category,
            user_notes=tx.user_notes,
            created_at=tx.created_at,
        )


class TransactionFilter(BaseModel):
    """Transaction filter parameters"""
    bank_account_id: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    transaction_type: Optional[str] = None
    category: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    is_taxable: Optional[bool] = None
    is_deductible: Optional[bool] = None
    is_internal_transfer: Optional[bool] = None
    search: Optional[str] = None  # Search in description/counterparty


class TransactionList(BaseModel):
    """Paginated list of transactions"""
    items: List[TransactionResponse]
    total: int
    page: int
    per_page: int
    pages: int
    total_credits: float
    total_debits: float


class TransactionClassify(BaseModel):
    """Transaction classification request"""
    category: str
    sub_category: Optional[str] = None
    is_taxable: bool = True
    is_deductible: bool = False
    tax_category: Optional[str] = None


class TransactionSummary(BaseModel):
    """Transaction summary statistics"""
    total_transactions: int
    total_credits: float
    total_debits: float
    net_flow: float
    by_category: dict
    by_month: dict
    taxable_income: float
    deductible_expenses: float
    internal_transfers: int


class BulkClassifyRequest(BaseModel):
    """Bulk classification request"""
    transaction_ids: List[int]
    classification: TransactionClassify


class TransactionExportRequest(BaseModel):
    """Transaction export request"""
    filter: TransactionFilter
    format: str = Field(default="csv", pattern="^(csv|excel|pdf)$")
    include_categories: bool = True
    include_tax_info: bool = True
