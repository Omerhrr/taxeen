"""
Bank Account Model
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.base import Base, TimestampMixin


# Nigerian Bank Codes (CBN/NIBSS codes)
NIGERIAN_BANK_CODES = {
    "044": "Access Bank",
    "014": "Access Bank (Diamond)",
    "023": "Citibank Nigeria",
    "063": "CityCode Bank",
    "050": "Ecobank Nigeria",
    "214": "First City Monument Bank",
    "011": "First Bank of Nigeria",
    "070": "Fidelity Bank",
    "058": "Guaranty Trust Bank",
    "069": "Heritage Bank",
    "030": "Heritage Bank (Enterprise)",
    "301": "Jaiz Bank",
    "082": "Keystone Bank",
    "035": "Mainstreet Bank",
    "101": "Providus Bank",
    "221": "Stanbic IBTC Bank",
    "068": "Standard Chartered Bank",
    "232": "Sterling Bank",
    "032": "Union Bank of Nigeria",
    "033": "United Bank for Africa",
    "039": "Stanbic IBTC Bank",
    "215": "Unity Bank",
    "035": "Wema Bank",
    "057": "Zenith Bank",
    "100": "Kuda Bank",
    "999": "OPay",
    "1000": "Moniepoint MFB",
    "9999": "PalmPay",
    "090": "Kuda Bank",
    "076": "Polaris Bank",
    "052": "Parallex Bank",
    "084": "Rubies MFB",
    "505": "Mint MFB",
    "503": "Sparkle MFB",
}


class BankAccount(Base, TimestampMixin):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Bank Details
    bank_name = Column(String(100), nullable=False)
    bank_code = Column(String(10), nullable=True)
    account_number = Column(String(20), nullable=False)  # Encrypted or masked
    account_name = Column(String(255), nullable=True)
    account_type = Column(String(50), default="savings")  # savings, current
    currency = Column(String(3), default="NGN")
    notes = Column(Text, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_status = Column(String(20), default="pending")  # pending, verified, failed
    current_balance = Column(Float, default=0.0)
    last_sync = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="bank_accounts")
    transactions = relationship("Transaction", back_populates="bank_account", cascade="all, delete-orphan")
    statement_uploads = relationship("StatementUpload", back_populates="bank_account", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<BankAccount(id={self.id}, bank='{self.bank_name}', account='{self.account_number}')>"
    
    @property
    def masked_account_number(self):
        """Return masked account number for display"""
        if self.account_number and len(self.account_number) >= 4:
            return f"****{self.account_number[-4:]}"
        return self.account_number
    
    def to_dict(self):
        return {
            "id": self.id,
            "bank_name": self.bank_name,
            "bank_code": self.bank_code,
            "account_number": self.masked_account_number,
            "account_name": self.account_name,
            "account_type": self.account_type,
            "currency": self.currency,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "current_balance": self.current_balance,
        }
