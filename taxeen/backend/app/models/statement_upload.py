"""
Statement Upload Model
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.base import Base, TimestampMixin


class StatementUpload(Base, TimestampMixin):
    __tablename__ = "statement_uploads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    
    # Statement Details
    date_from = Column(String(20), nullable=True)
    date_to = Column(String(20), nullable=True)
    json_path = Column(String(255), nullable=True)
    md_path = Column(String(255), nullable=True)
    
    # Status
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    transactions_count = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="statement_uploads")
    bank_account = relationship("BankAccount", back_populates="statement_uploads")
    
    def __repr__(self):
        return f"<StatementUpload(id={self.id}, status='{self.status}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "status": self.status,
            "transactions_count": self.transactions_count,
        }
