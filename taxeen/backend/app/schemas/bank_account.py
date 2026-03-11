"""
Bank Account Schemas
Request/Response models for bank account endpoints
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class BankAccountBase(BaseModel):
    """Base bank account schema"""
    bank_name: str = Field(..., min_length=2, max_length=100)
    account_number: str = Field(..., min_length=10, max_length=10)
    account_name: str = Field(..., min_length=2, max_length=255)
    account_type: str = Field(default="Savings", pattern="^(Savings|Current|Domiciliary|Corporate)$")
    
    @field_validator('account_number')
    @classmethod
    def validate_account_number(cls, v):
        if not v.isdigit():
            raise ValueError('Account number must contain only digits')
        return v


class BankAccountCreate(BankAccountBase):
    """Bank account creation schema"""
    bank_code: Optional[str] = Field(None, max_length=10)
    currency: str = Field(default="NGN", max_length=3)
    notes: Optional[str] = Field(None, max_length=500)


class BankAccountUpdate(BaseModel):
    """Bank account update schema"""
    account_name: Optional[str] = Field(None, min_length=2, max_length=255)
    account_type: Optional[str] = Field(None, pattern="^(Savings|Current|Domiciliary|Corporate)$")
    notes: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class BankAccountResponse(BaseModel):
    """Bank account response schema"""
    id: int
    bank_name: str
    account_number: str  # Masked for security
    account_name: str
    account_type: str
    currency: str
    current_balance: float
    is_active: bool
    is_verified: bool
    last_sync: Optional[datetime] = None
    created_at: datetime
    transactions_count: Optional[int] = 0
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_orm(cls, account, transactions_count: int = 0):
        """Create response from ORM model"""
        # Mask account number
        masked = f"****{account.account_number[-4:]}" if len(account.account_number) >= 4 else "****"
        return cls(
            id=account.id,
            bank_name=account.bank_name,
            account_number=masked,
            account_name=account.account_name,
            account_type=account.account_type,
            currency=account.currency,
            current_balance=account.current_balance,
            is_active=account.is_active,
            is_verified=account.is_verified,
            last_sync=account.last_sync,
            created_at=account.created_at,
            transactions_count=transactions_count,
        )


class BankAccountList(BaseModel):
    """List of bank accounts with summary"""
    accounts: List[BankAccountResponse]
    total: int
    total_balance: float


class BankAccountDetail(BankAccountResponse):
    """Detailed bank account with recent transactions"""
    recent_transactions: List[dict] = []
    statement_uploads_count: int = 0
    last_statement_date: Optional[datetime] = None


class BankVerificationRequest(BaseModel):
    """Bank account verification request"""
    bank_code: str
    account_number: str


class BankVerificationResponse(BaseModel):
    """Bank account verification response"""
    verified: bool
    account_name: Optional[str] = None
    account_number: Optional[str] = None
    bank_name: Optional[str] = None
    message: Optional[str] = None
