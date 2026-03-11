"""
Authentication API Routes
Register, Login, Logout, Token Refresh
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from app.database import get_db
from app.models import User
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
    get_current_user,
    encrypt_nin,
    decrypt_nin,
)
from app.config import settings
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.schemas.auth import (
    Token,
    TokenRefresh,
    LoginResponse,
    PasswordChange,
    SubscriptionStatus,
)
from app.schemas.common import MessageResponse, ErrorResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user account
    
    - Validates email uniqueness
    - Hashes password with Argon2
    - Encrypts NIN with AES-256 if provided
    - Returns access tokens and user info
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    password_hash = hash_password(user_data.password)
    
    # Encrypt NIN if provided
    nin_encrypted = None
    nin_iv = None
    if user_data.nin:
        nin_encrypted, nin_iv = encrypt_nin(user_data.nin)
    
    # Create user
    user = User(
        email=user_data.email,
        password_hash=password_hash,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        nin_encrypted=nin_encrypted,
        nin_iv=nin_iv,
        subscription_plan="free",
        subscription_status="active",
        is_active=True,
        is_verified=False,
        is_admin=False,
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Generate tokens
    token_data = {"sub": str(user.id), "email": user.email}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.from_orm(user)
    )


@router.post("/login", response_model=LoginResponse)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return tokens
    
    - Validates credentials
    - Returns access and refresh tokens
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(user.password_hash, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )
    
    # Generate tokens
    token_data = {"sub": str(user.id), "email": user.email}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.from_orm(user)
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    
    - Validates refresh token
    - Returns new access and refresh tokens
    """
    payload = verify_token(token_data.refresh_token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate new tokens
    new_token_data = {"sub": str(user.id), "email": user.email}
    access_token = create_access_token(new_token_data)
    refresh_token = create_refresh_token(new_token_data)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user = Depends(get_current_user)
):
    """
    Logout user (invalidate tokens on client side)
    
    Note: With JWT, actual token invalidation requires a blacklist.
    For now, clients should discard their tokens.
    """
    # In a production system, you would add the token to a blacklist
    # For now, we just return success
    return MessageResponse(message="Successfully logged out")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user = Depends(get_current_user)
):
    """
    Get current authenticated user information
    """
    return UserResponse.from_orm(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    update_data: UserUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile
    """
    if update_data.first_name:
        current_user.first_name = update_data.first_name
    if update_data.last_name:
        current_user.last_name = update_data.last_name
    if update_data.phone is not None:
        current_user.phone = update_data.phone
    if update_data.tax_id is not None:
        current_user.tax_id = update_data.tax_id
    
    db.commit()
    db.refresh(current_user)
    
    return UserResponse.from_orm(current_user)


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    password_data: PasswordChange,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user password
    
    - Validates current password
    - Updates to new password
    """
    # Verify current password
    if not verify_password(current_user.password_hash, password_data.current_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Validate new password matches confirmation
    if not password_data.passwords_match():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New passwords do not match"
        )
    
    # Update password
    current_user.password_hash = hash_password(password_data.new_password)
    db.commit()
    
    return MessageResponse(message="Password changed successfully")


@router.get("/subscription", response_model=SubscriptionStatus)
async def get_subscription_status(
    current_user = Depends(get_current_user)
):
    """
    Get user subscription status
    """
    days_remaining = None
    if current_user.subscription_expires:
        delta = current_user.subscription_expires - datetime.utcnow()
        days_remaining = max(0, delta.days)
    
    features = {
        "free": {"transactions": 100, "bank_accounts": 1, "reports": 1},
        "basic": {"transactions": 1000, "bank_accounts": 3, "reports": 12},
        "premium": {"transactions": -1, "bank_accounts": -1, "reports": -1},
        "enterprise": {"transactions": -1, "bank_accounts": -1, "reports": -1},
    }
    
    return SubscriptionStatus(
        plan=current_user.subscription_plan,
        status=current_user.subscription_status,
        expires_at=current_user.subscription_expires.isoformat() if current_user.subscription_expires else None,
        days_remaining=days_remaining,
        features=features.get(current_user.subscription_plan, features["free"])
    )


@router.post("/activate", response_model=MessageResponse)
async def activate_subscription(
    plan: str,
    payment_reference: Optional[str] = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Activate subscription plan
    
    In production, this would verify payment with Paystack
    """
    valid_plans = ["free", "basic", "premium", "enterprise"]
    if plan not in valid_plans:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid plan. Choose from: {', '.join(valid_plans)}"
        )
    
    # Set subscription (mock - in production, verify with Paystack)
    current_user.subscription_plan = plan
    current_user.subscription_status = "active"
    
    # Set expiry based on plan
    if plan != "free":
        current_user.subscription_expires = datetime.utcnow() + timedelta(days=30)
    else:
        current_user.subscription_expires = None
    
    db.commit()
    
    return MessageResponse(message=f"Subscription activated: {plan}")
