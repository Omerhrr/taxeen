"""
Auth Schemas
Request/Response models for authentication endpoints
"""

from typing import Optional
from pydantic import BaseModel, Field
from .user import UserResponse


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Token expiration in seconds")


class TokenRefresh(BaseModel):
    """Token refresh request"""
    refresh_token: str


class LoginResponse(BaseModel):
    """Login response with tokens and user info"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class PasswordChange(BaseModel):
    """Password change request"""
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    
    def passwords_match(self) -> bool:
        """Check if new passwords match"""
        return self.new_password == self.confirm_password


class PasswordResetRequest(BaseModel):
    """Password reset request"""
    email: str


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation"""
    token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)


class EmailVerification(BaseModel):
    """Email verification request"""
    token: str


class ActivateSubscription(BaseModel):
    """Subscription activation request"""
    plan: str = Field(..., pattern="^(basic|premium|enterprise)$")
    payment_reference: Optional[str] = None


class SubscriptionStatus(BaseModel):
    """Subscription status response"""
    plan: str
    status: str
    expires_at: Optional[str] = None
    days_remaining: Optional[int] = None
    features: dict = {}
