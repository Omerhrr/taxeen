"""
Statement Upload Model
Handles bank statement uploads and processing
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from app.database import Base, TimestampMixin
import enum


class UploadStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StatementUpload(Base, TimestampMixin):
    __tablename__ = "statement_uploads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    
    # File Details
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=True)  # Encrypted storage path
    file_size = Column(Integer, nullable=True)  # in bytes
    file_hash = Column(String(64), nullable=True)  # SHA-256 hash for deduplication
    
    # Statement Period
    statement_start_date = Column(DateTime, nullable=True)
    statement_end_date = Column(DateTime, nullable=True)
    statement_date = Column(DateTime, nullable=True)  # Date statement was generated
    
    # Processing Status
    status = Column(String(20), default="pending")
    processing_started = Column(DateTime, nullable=True)
    processing_completed = Column(DateTime, nullable=True)
    
    # Processing Results
    total_transactions = Column(Integer, default=0)
    total_credits = Column(Float, default=0.0)
    total_debits = Column(Float, default=0.0)
    opening_balance = Column(Float, nullable=True)
    closing_balance = Column(Float, nullable=True)
    
    # Processing Details
    extraction_method = Column(String(50), default="pdfplumber")  # pdfplumber, ocr, manual
    parsing_errors = Column(Text, nullable=True)  # JSON array of errors
    warnings = Column(Text, nullable=True)  # JSON array of warnings
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verified_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    verification_date = Column(DateTime, nullable=True)
    verification_notes = Column(Text, nullable=True)
    
    # Metadata
    notes = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="statement_uploads")
    bank_account = relationship("BankAccount", back_populates="statement_uploads")
    transactions = relationship("Transaction", back_populates="statement_upload")
    
    def __repr__(self):
        return f"<StatementUpload(id={self.id}, file='{self.file_name}', status='{self.status}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "file_name": self.file_name,
            "status": self.status,
            "statement_start_date": self.statement_start_date.isoformat() if self.statement_start_date else None,
            "statement_end_date": self.statement_end_date.isoformat() if self.statement_end_date else None,
            "total_transactions": self.total_transactions,
            "total_credits": self.total_credits,
            "total_debits": self.total_debits,
            "opening_balance": self.opening_balance,
            "closing_balance": self.closing_balance,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
