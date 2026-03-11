"""
Database Configuration for Taxeen
SQLAlchemy setup with SQLite (dev) / PostgreSQL (prod)
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Database URL from environment or default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taxeen.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    # Import Base and all models here to avoid circular imports
    from app.base import Base
    from app.models import User, BankAccount, Transaction, StatementUpload
    
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized")
