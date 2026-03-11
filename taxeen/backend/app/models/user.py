"""
User Model
Handles user registration with NIN encryption
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from app.base import Base, TimestampMixin
from datetime import datetime


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Personal Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    
    # NIN (National Identity Number) - Encrypted with AES-256
    nin_encrypted = Column(Text, nullable=True)
    nin_iv = Column(String(64), nullable=True)  # Initialization vector for AES
    
    # Subscription
    subscription_plan = Column(String(50), default="free")  # free, basic, premium, enterprise
    subscription_status = Column(String(50), default="active")
    subscription_expires = Column(DateTime, nullable=True)
    paystack_customer_id = Column(String(100), nullable=True)
    
    # Account Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    
    # Profile
    profile_picture = Column(String(255), nullable=True)
    tax_id = Column(String(50), nullable=True)  # Nigerian Tax Identification Number
    
    # Relationships
    bank_accounts = relationship("BankAccount", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    statement_uploads = relationship("StatementUpload", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', name='{self.first_name} {self.last_name}')>"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "subscription_plan": self.subscription_plan,
            "subscription_status": self.subscription_status,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
