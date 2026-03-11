"""
Transaction Model
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.base import Base, TimestampMixin


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    
    # Transaction Details
    date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    direction = Column(String(10), nullable=False)  # credit or debit
    balance = Column(Float, nullable=True)
    
    # Classification
    category = Column(String(50), default="uncategorized")
    is_internal_transfer = Column(Boolean, default=False)
    is_income = Column(Boolean, default=False)
    is_expense = Column(Boolean, default=False)
    taxable = Column(Boolean, default=True)
    
    # Additional
    reference = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    bank_account = relationship("BankAccount", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, direction='{self.direction}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "date": str(self.date) if self.date else None,
            "description": self.description,
            "amount": self.amount,
            "direction": self.direction,
            "balance": self.balance,
            "category": self.category,
            "is_internal_transfer": self.is_internal_transfer,
            "taxable": self.taxable,
        }
