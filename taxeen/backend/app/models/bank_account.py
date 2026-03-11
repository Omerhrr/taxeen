"""
Bank Account Model
Manages user bank accounts
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base, TimestampMixin
import enum


class BankType(enum.Enum):
    """Nigerian Banks"""
    ACCESS = "Access Bank"
    FIRST = "First Bank of Nigeria"
    GTB = "Guaranty Trust Bank"
    UBA = "United Bank for Africa"
    ZENITH = "Zenith Bank"
    STANBIC = "Stanbic IBTC Bank"
    FIDELITY = "Fidelity Bank"
    UNION = "Union Bank of Nigeria"
    ECOBANK = "Ecobank Nigeria"
    WEMA = "Wema Bank"
    STERLING = "Sterling Bank"
    FCMB = "First City Monument Bank"
    PROVIDUS = "Providus Bank"
    UNITY = "Unity Bank"
    POLARIS = "Polaris Bank"
    KEYSTONE = "Keystone Bank"
    JAIZ = "Jaiz Bank"
    TAJ = "TAJ Bank"
    LOTUS = "Lotus Bank"
    TITAN = "Titan Trust Bank"
    OPAY = "OPay"
    KUDA = "Kuda Bank"
    MONIEPOINT = "Moniepoint MFB"
    PALMPAY = "PalmPay"
    OTHER = "Other"


class AccountType(enum.Enum):
    SAVINGS = "Savings"
    CURRENT = "Current"
    DOMICILIARY = "Domiciliary"
    CORPORATE = "Corporate"


class BankAccount(Base, TimestampMixin):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Bank Details
    bank_name = Column(String(100), nullable=False)
    bank_code = Column(String(10), nullable=True)  # CBN bank code
    account_number = Column(String(20), nullable=False)  # Encrypted
    account_name = Column(String(255), nullable=False)
    account_type = Column(String(50), default="Savings")
    
    # Account Info
    currency = Column(String(3), default="NGN")
    current_balance = Column(Float, default=0.0)
    last_sync = Column(DateTime, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_status = Column(String(50), default="pending")
    
    # Metadata
    notes = Column(String(500), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="bank_accounts")
    transactions = relationship("Transaction", back_populates="bank_account", cascade="all, delete-orphan")
    statement_uploads = relationship("StatementUpload", back_populates="bank_account", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<BankAccount(id={self.id}, bank='{self.bank_name}', account='****{self.account_number[-4:] if self.account_number else '****'}')>"
    
    @property
    def masked_account_number(self):
        """Return masked account number for display"""
        if self.account_number and len(self.account_number) >= 4:
            return f"****{self.account_number[-4:]}"
        return "****"
    
    def to_dict(self):
        return {
            "id": self.id,
            "bank_name": self.bank_name,
            "account_number": self.masked_account_number,
            "account_name": self.account_name,
            "account_type": self.account_type,
            "currency": self.currency,
            "current_balance": self.current_balance,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
        }


# Nigerian bank codes for verification
NIGERIAN_BANK_CODES = {
    "044": "Access Bank",
    "011": "First Bank of Nigeria",
    "058": "Guaranty Trust Bank",
    "033": "United Bank for Africa",
    "057": "Zenith Bank",
    "039": "Stanbic IBTC Bank",
    "070": "Fidelity Bank",
    "032": "Union Bank of Nigeria",
    "050": "Ecobank Nigeria",
    "035": "Wema Bank",
    "232": "Sterling Bank",
    "214": "First City Monument Bank",
    "101": "Providus Bank",
    "215": "Unity Bank",
    "076": "Polaris Bank",
    "082": "Keystone Bank",
    "301": "Jaiz Bank",
    "302": "TAJ Bank",
    "303": "Lotus Bank",
    "102": "Titan Trust Bank",
    "999": "OPay",
    "090": "Kuda Bank",
    "100": "Moniepoint MFB",
    "9999": "PalmPay",
}
