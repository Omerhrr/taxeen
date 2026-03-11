"""
Transaction Model
Handles bank transactions and classification
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.database import Base, TimestampMixin
import enum
from datetime import datetime


class TransactionType(enum.Enum):
    CREDIT = "credit"
    DEBIT = "debit"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
    INTERNAL_TRANSFER = "internal_transfer"


class TransactionCategory(enum.Enum):
    """Transaction categories for tax purposes"""
    SALARY = "salary"
    BUSINESS_INCOME = "business_income"
    INVESTMENT = "investment"
    RENTAL_INCOME = "rental_income"
    OTHER_INCOME = "other_income"
    
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
    OTHER_EXPENSE = "other_expense"
    
    UNCATEGORIZED = "uncategorized"


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    statement_upload_id = Column(Integer, ForeignKey("statement_uploads.id"), nullable=True)
    
    # Transaction Details
    transaction_date = Column(DateTime, nullable=False, index=True)
    value_date = Column(DateTime, nullable=True)
    transaction_type = Column(String(20), nullable=False)  # credit, debit
    amount = Column(Float, nullable=False)
    balance = Column(Float, nullable=True)  # Balance after transaction
    
    # Description
    description = Column(Text, nullable=True)
    reference = Column(String(100), nullable=True)
    narration = Column(Text, nullable=True)
    
    # Counterparty
    counterparty_name = Column(String(255), nullable=True)
    counterparty_account = Column(String(50), nullable=True)
    counterparty_bank = Column(String(100), nullable=True)
    
    # Classification
    category = Column(String(50), default="uncategorized")
    sub_category = Column(String(50), nullable=True)
    is_taxable = Column(Boolean, default=True)
    is_deductible = Column(Boolean, default=False)
    tax_category = Column(String(50), nullable=True)
    
    # Internal Transfer Detection
    is_internal_transfer = Column(Boolean, default=False)
    related_transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)
    related_bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=True)
    
    # Status
    is_verified = Column(Boolean, default=False)
    verification_notes = Column(Text, nullable=True)
    
    # User notes
    user_notes = Column(Text, nullable=True)
    user_tags = Column(String(255), nullable=True)  # JSON array of tags
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    bank_account = relationship("BankAccount", back_populates="transactions", foreign_keys=[bank_account_id])
    statement_upload = relationship("StatementUpload", back_populates="transactions")
    related_transaction = relationship("Transaction", remote_side=[id], foreign_keys=[related_transaction_id])
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, date='{self.transaction_date}', type='{self.transaction_type}', amount={self.amount})>"
    
    @property
    def formatted_amount(self):
        """Return formatted amount with currency symbol"""
        return f"₦{self.amount:,.2f}"
    
    @property
    def is_income(self):
        """Check if transaction is income"""
        return self.transaction_type in ["credit", "transfer_in"]
    
    @property
    def is_expense(self):
        """Check if transaction is expense"""
        return self.transaction_type in ["debit", "transfer_out"]
    
    def to_dict(self):
        return {
            "id": self.id,
            "transaction_date": self.transaction_date.isoformat() if self.transaction_date else None,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "formatted_amount": self.formatted_amount,
            "description": self.description,
            "category": self.category,
            "counterparty_name": self.counterparty_name,
            "is_internal_transfer": self.is_internal_transfer,
            "is_taxable": self.is_taxable,
            "is_deductible": self.is_deductible,
            "balance": self.balance,
        }
