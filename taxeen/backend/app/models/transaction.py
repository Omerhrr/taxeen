"""
Transaction Model
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from app.base import Base, TimestampMixin


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    
    # Transaction Details
    transaction_date = Column(Date, nullable=False)  # Date of transaction
    description = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(20), nullable=False)  # credit, debit, transfer_in, transfer_out
    direction = Column(String(10), nullable=False)  # credit or debit
    balance = Column(Float, nullable=True)
    
    # Counterparty
    counterparty_name = Column(String(255), nullable=True)
    counterparty_account = Column(String(20), nullable=True)
    reference = Column(String(100), nullable=True)
    
    # Classification
    category = Column(String(50), default="uncategorized")
    sub_category = Column(String(50), nullable=True)
    
    # Tax-related
    is_income = Column(Boolean, default=False)
    is_expense = Column(Boolean, default=False)
    is_internal_transfer = Column(Boolean, default=False)
    is_taxable = Column(Boolean, default=True)
    is_deductible = Column(Boolean, default=False)
    tax_category = Column(String(50), nullable=True)
    
    # User customization
    user_notes = Column(Text, nullable=True)
    user_tags = Column(JSON, nullable=True)  # List of tags
    
    # Internal transfer tracking
    related_transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)
    related_bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=True)
    
    # Raw data
    raw_data = Column(JSON, nullable=True)  # Original transaction data from statement
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    bank_account = relationship("BankAccount", back_populates="transactions", foreign_keys=[bank_account_id])
    related_bank_account = relationship("BankAccount", foreign_keys=[related_bank_account_id])
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, direction='{self.direction}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "date": str(self.transaction_date) if self.transaction_date else None,
            "description": self.description,
            "amount": self.amount,
            "transaction_type": self.transaction_type,
            "direction": self.direction,
            "balance": self.balance,
            "category": self.category,
            "sub_category": self.sub_category,
            "counterparty_name": self.counterparty_name,
            "is_internal_transfer": self.is_internal_transfer,
            "is_taxable": self.is_taxable,
            "is_deductible": self.is_deductible,
            "tax_category": self.tax_category,
        }
