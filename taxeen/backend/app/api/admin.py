"""
Admin API Routes
Admin panel endpoints for user and subscription management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.models import User, BankAccount, Transaction, StatementUpload
from app.auth import get_current_admin_user
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.common import MessageResponse, PaginatedResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard")
async def get_admin_dashboard(
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get admin dashboard statistics
    """
    # User statistics
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    verified_users = db.query(User).filter(User.is_verified == True).count()
    new_users_this_month = db.query(User).filter(
        User.created_at >= datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
    ).count()
    
    # Subscription statistics
    subscription_stats = db.query(
        User.subscription_plan,
        func.count(User.id)
    ).group_by(User.subscription_plan).all()
    
    subscription_counts = {plan: count for plan, count in subscription_stats}
    
    # Active subscriptions
    active_subscriptions = db.query(User).filter(
        User.subscription_status == "active",
        User.subscription_expires > datetime.utcnow()
    ).count()
    
    # Expiring soon (within 7 days)
    expiring_soon = db.query(User).filter(
        User.subscription_status == "active",
        User.subscription_expires.between(
            datetime.utcnow(),
            datetime.utcnow() + timedelta(days=7)
        )
    ).count()
    
    # Transaction statistics
    total_transactions = db.query(Transaction).count()
    transactions_this_month = db.query(Transaction).filter(
        Transaction.created_at >= datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
    ).count()
    
    # Statement uploads
    total_uploads = db.query(StatementUpload).count()
    uploads_this_month = db.query(StatementUpload).filter(
        StatementUpload.created_at >= datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
    ).count()
    
    # Processing status
    pending_uploads = db.query(StatementUpload).filter(
        StatementUpload.status == "pending"
    ).count()
    
    processing_uploads = db.query(StatementUpload).filter(
        StatementUpload.status == "processing"
    ).count()
    
    # Bank accounts
    total_bank_accounts = db.query(BankAccount).count()
    verified_bank_accounts = db.query(BankAccount).filter(
        BankAccount.is_verified == True
    ).count()
    
    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "verified": verified_users,
            "new_this_month": new_users_this_month,
        },
        "subscriptions": {
            "by_plan": subscription_counts,
            "active": active_subscriptions,
            "expiring_soon": expiring_soon,
        },
        "transactions": {
            "total": total_transactions,
            "this_month": transactions_this_month,
        },
        "uploads": {
            "total": total_uploads,
            "this_month": uploads_this_month,
            "pending": pending_uploads,
            "processing": processing_uploads,
        },
        "bank_accounts": {
            "total": total_bank_accounts,
            "verified": verified_bank_accounts,
        },
    }


@router.get("/users", response_model=PaginatedResponse)
async def list_users(
    search: Optional[str] = None,
    subscription_plan: Optional[str] = None,
    subscription_status: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_verified: Optional[bool] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    List all users with filtering options
    """
    query = db.query(User)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (User.email.ilike(search_pattern)) |
            (User.first_name.ilike(search_pattern)) |
            (User.last_name.ilike(search_pattern))
        )
    
    if subscription_plan:
        query = query.filter(User.subscription_plan == subscription_plan)
    
    if subscription_status:
        query = query.filter(User.subscription_status == subscription_status)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    if is_verified is not None:
        query = query.filter(User.is_verified == is_verified)
    
    total = query.count()
    
    offset = (page - 1) * per_page
    users = query.order_by(User.created_at.desc()).offset(offset).limit(per_page).all()
    
    pages = (total + per_page - 1) // per_page
    
    return PaginatedResponse(
        items=[UserResponse.from_orm(u) for u in users],
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
    )


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get user details
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.from_orm(user)


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    update_data: UserUpdate,
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update user details (admin)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if update_data.first_name:
        user.first_name = update_data.first_name
    if update_data.last_name:
        user.last_name = update_data.last_name
    if update_data.phone is not None:
        user.phone = update_data.phone
    if update_data.tax_id is not None:
        user.tax_id = update_data.tax_id
    
    db.commit()
    db.refresh(user)
    
    return UserResponse.from_orm(user)


@router.post("/users/{user_id}/activate", response_model=MessageResponse)
async def activate_user(
    user_id: int,
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Activate user account
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = True
    db.commit()
    
    return MessageResponse(message=f"User {user.email} activated")


@router.post("/users/{user_id}/deactivate", response_model=MessageResponse)
async def deactivate_user(
    user_id: int,
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Deactivate user account
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = False
    db.commit()
    
    return MessageResponse(message=f"User {user.email} deactivated")


@router.post("/users/{user_id}/verify", response_model=MessageResponse)
async def verify_user(
    user_id: int,
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Verify user account
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_verified = True
    db.commit()
    
    return MessageResponse(message=f"User {user.email} verified")


@router.post("/users/{user_id}/subscription", response_model=MessageResponse)
async def update_user_subscription(
    user_id: int,
    plan: str,
    months: int = 1,
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update user subscription (admin override)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    valid_plans = ["free", "basic", "premium", "enterprise"]
    if plan not in valid_plans:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid plan. Choose from: {', '.join(valid_plans)}"
        )
    
    user.subscription_plan = plan
    user.subscription_status = "active"
    
    if plan != "free":
        user.subscription_expires = datetime.utcnow() + timedelta(days=30 * months)
    else:
        user.subscription_expires = None
    
    db.commit()
    
    return MessageResponse(
        message=f"User {user.email} subscription updated to {plan} for {months} month(s)"
    )


@router.get("/users/{user_id}/activity")
async def get_user_activity(
    user_id: int,
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get user activity summary
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get activity metrics
    bank_accounts = db.query(BankAccount).filter(
        BankAccount.user_id == user_id
    ).count()
    
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).count()
    
    uploads = db.query(StatementUpload).filter(
        StatementUpload.user_id == user_id
    ).count()
    
    # Last activity
    last_transaction = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).order_by(Transaction.created_at.desc()).first()
    
    last_upload = db.query(StatementUpload).filter(
        StatementUpload.user_id == user_id
    ).order_by(StatementUpload.created_at.desc()).first()
    
    return {
        "user_id": user_id,
        "email": user.email,
        "bank_accounts_count": bank_accounts,
        "transactions_count": transactions,
        "uploads_count": uploads,
        "last_transaction": last_transaction.created_at.isoformat() if last_transaction else None,
        "last_upload": last_upload.created_at.isoformat() if last_upload else None,
        "account_age_days": (datetime.utcnow() - user.created_at).days,
    }


@router.get("/subscriptions/expiring")
async def get_expiring_subscriptions(
    days: int = Query(7, ge=1, le=30),
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get subscriptions expiring within specified days
    """
    users = db.query(User).filter(
        User.subscription_status == "active",
        User.subscription_expires.between(
            datetime.utcnow(),
            datetime.utcnow() + timedelta(days=days)
        )
    ).all()
    
    return {
        "days": days,
        "count": len(users),
        "users": [
            {
                "id": u.id,
                "email": u.email,
                "name": u.full_name,
                "plan": u.subscription_plan,
                "expires": u.subscription_expires.isoformat(),
                "days_remaining": (u.subscription_expires - datetime.utcnow()).days,
            }
            for u in users
        ]
    }


@router.get("/subscriptions/stats")
async def get_subscription_stats(
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get subscription statistics by plan
    """
    # By plan
    by_plan = db.query(
        User.subscription_plan,
        func.count(User.id)
    ).group_by(User.subscription_plan).all()
    
    # By status
    by_status = db.query(
        User.subscription_status,
        func.count(User.id)
    ).group_by(User.subscription_status).all()
    
    # Revenue estimation (simplified)
    plan_prices = {
        "basic": 2500,
        "premium": 5000,
        "enterprise": 15000,
    }
    
    estimated_monthly_revenue = 0
    for plan, count in by_plan:
        if plan in plan_prices:
            estimated_monthly_revenue += plan_prices[plan] * count
    
    return {
        "by_plan": {plan: count for plan, count in by_plan},
        "by_status": {status: count for status, count in by_status},
        "estimated_monthly_revenue": estimated_monthly_revenue,
    }


@router.get("/uploads/pending")
async def get_pending_uploads(
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get pending statement uploads that need processing
    """
    uploads = db.query(StatementUpload).filter(
        StatementUpload.status.in_(["pending", "processing"])
    ).order_by(StatementUpload.created_at).all()
    
    return {
        "count": len(uploads),
        "uploads": [
            {
                "id": u.id,
                "user_id": u.user_id,
                "file_name": u.file_name,
                "status": u.status,
                "created_at": u.created_at.isoformat(),
                "processing_time": (
                    (datetime.utcnow() - u.processing_started).total_seconds()
                    if u.processing_started else None
                ),
            }
            for u in uploads
        ]
    }


@router.post("/make-admin/{user_id}", response_model=MessageResponse)
async def make_admin(
    user_id: int,
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Grant admin privileges to a user
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_admin = True
    db.commit()
    
    return MessageResponse(message=f"User {user.email} is now an admin")


@router.delete("/users/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: int,
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete a user account and all associated data
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete admin user"
        )
    
    email = user.email
    db.delete(user)
    db.commit()
    
    return MessageResponse(message=f"User {email} deleted")
