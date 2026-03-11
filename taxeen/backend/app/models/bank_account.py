"""
Bank Account Model
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.base import Base, TimestampMixin


class BankAccount(Base, TimestampMixin):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Bank Details
    bank_name = Column(String(100), nullable=False)
    account_number = Column(String(20), nullable=False)  # Encrypted or masked
    account_name = Column(String(255), nullable=True)
    account_type = Column(String(50), default="savings")  # savings, current
    
    # Status
    is_active = Column(Boolean, default=True)
    current_balance = Column(Float, default=0.0)
    last_sync = Column(String(50), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="bank_accounts")
    transactions = relationship("Transaction", back_populates="bank_account", cascade="all, delete-orphan")
    statement_uploads = relationship("StatementUpload", back_populates="bank_account", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<BankAccount(id={self.id}, bank='{self.bank_name}', account='{self.account_number}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "bank_name": self.bank_name,
            "account_number": self.account_number,
            "account_name": self.account_name,
            "account_type": self.account_type,
            "is_active": self.is_active,
            "current_balance": self.current_balance,
        }
