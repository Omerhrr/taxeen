"""
Statement Schemas
Request/Response models for statement upload endpoints
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class StatementUploadResponse(BaseModel):
    """Statement upload response"""
    id: int
    user_id: int
    bank_account_id: int
    file_name: str
    status: str
    statement_start_date: Optional[datetime] = None
    statement_end_date: Optional[datetime] = None
    total_transactions: int
    total_credits: float
    total_debits: float
    opening_balance: Optional[float] = None
    closing_balance: Optional[float] = None
    extraction_method: Optional[str] = None
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class StatementList(BaseModel):
    """List of statement uploads"""
    items: List[StatementUploadResponse]
    total: int
    page: int
    per_page: int
    pages: int


class StatementProcessRequest(BaseModel):
    """Statement processing request"""
    bank_account_id: int
    statement_start_date: Optional[datetime] = None
    statement_end_date: Optional[datetime] = None


class StatementDetail(StatementUploadResponse):
    """Detailed statement with processing info"""
    parsing_errors: Optional[List[dict]] = None
    warnings: Optional[List[str]] = None
    processing_started: Optional[datetime] = None
    processing_completed: Optional[datetime] = None
    verification_notes: Optional[str] = None


class StatementVerifyRequest(BaseModel):
    """Statement verification request"""
    verified: bool
    notes: Optional[str] = None


class ParsedTransaction(BaseModel):
    """Parsed transaction from statement"""
    date: datetime
    description: str
    amount: float
    balance: Optional[float] = None
    transaction_type: str
    reference: Optional[str] = None
    value_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ParseResult(BaseModel):
    """Result of statement parsing"""
    success: bool
    total_transactions: int
    total_credits: float
    total_debits: float
    opening_balance: Optional[float] = None
    closing_balance: Optional[float] = None
    statement_start_date: Optional[datetime] = None
    statement_end_date: Optional[datetime] = None
    transactions: List[ParsedTransaction] = []
    errors: List[str] = []
    warnings: List[str] = []
    extraction_method: str = "pdfplumber"


class BankStatementUpload(BaseModel):
    """Bank statement upload metadata"""
    bank_account_id: int
    file_name: str
    file_size: int
    file_hash: Optional[str] = None
