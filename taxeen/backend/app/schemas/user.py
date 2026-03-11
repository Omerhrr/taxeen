"""
User Schemas
Request/Response models for user endpoints
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator
import re


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)


class UserCreate(UserBase):
    """User registration schema"""
    password: str = Field(..., min_length=8, max_length=128)
    nin: Optional[str] = Field(None, description="Nigerian National Identity Number (11 digits)")
    
    @field_validator('nin')
    @classmethod
    def validate_nin(cls, v):
        if v is not None:
            # Remove any spaces or dashes
            v = v.replace(' ', '').replace('-', '')
            if not v.isdigit() or len(v) != 11:
                raise ValueError('NIN must be exactly 11 digits')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """User update schema"""
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    tax_id: Optional[str] = Field(None, max_length=50)


class UserResponse(BaseModel):
    """User response schema"""
    id: int
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    full_name: str
    subscription_plan: str = "free"
    subscription_status: str = "active"
    subscription_expires: Optional[datetime] = None
    is_active: bool = True
    is_verified: bool = False
    is_admin: bool = False
    tax_id: Optional[str] = None
    has_nin: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_orm(cls, user):
        """Create response from ORM model"""
        return cls(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            full_name=user.full_name,
            subscription_plan=user.subscription_plan,
            subscription_status=user.subscription_status,
            subscription_expires=user.subscription_expires,
            is_active=user.is_active,
            is_verified=user.is_verified,
            is_admin=user.is_admin,
            tax_id=user.tax_id,
            has_nin=bool(user.nin_encrypted),
            created_at=user.created_at,
        )


class UserWithSubscription(UserResponse):
    """User response with subscription details"""
    subscription_days_remaining: Optional[int] = None
    transactions_count: int = 0
    bank_accounts_count: int = 0


class UserProfile(BaseModel):
    """User profile with extended information"""
    id: int
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    tax_id: Optional[str] = None
    subscription_plan: str
    subscription_status: str
    subscription_expires: Optional[datetime] = None
    is_verified: bool
    created_at: datetime
    bank_accounts_count: int = 0
    transactions_count: int = 0
    statements_count: int = 0
    
    class Config:
        from_attributes = True
