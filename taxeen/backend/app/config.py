"""
Taxeen Configuration
Environment-based configuration settings
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Application
    APP_NAME: str = "Taxeen"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "sqlite:///./taxeen.db"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # AES-256 Encryption (for NIN)
    AES_SECRET_KEY: str = "aes-256-secret-key-32-bytes-long!!"  # Must be 32 bytes for AES-256
    
    # Password Hashing (Argon2)
    ARGON2_TIME_COST: int = 3
    ARGON2_MEMORY_COST: int = 65536
    ARGON2_PARALLELISM: int = 4
    ARGON2_HASH_LENGTH: int = 32
    ARGON2_SALT_LENGTH: int = 16
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: str = "pdf,PDF"
    
    # Paystack (Payment Gateway)
    PAYSTACK_SECRET_KEY: Optional[str] = None
    PAYSTACK_PUBLIC_KEY: Optional[str] = None
    PAYSTACK_WEBHOOK_SECRET: Optional[str] = None
    
    # Email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@taxeen.ng"
    
    # CORS
    CORS_ORIGINS: str = "*"
    
    # Tax Configuration (Nigeria 2026)
    TAX_FREE_THRESHOLD: float = 800000.0  # First ₦800,000 is tax-free
    RENT_RELIEF_MAX: float = 500000.0  # Maximum rent relief
    RENT_RELIEF_PERCENTAGE: float = 0.20  # 20% of annual rent
    
    # Tax Bands (Nigeria 2026)
    # Format: (upper_limit, rate)
    TAX_BANDS: list = [
        (800000, 0.0),           # 0 - 800,000 → 0%
        (3000000, 0.15),         # 800,001 - 3,000,000 → 15%
        (12000000, 0.18),        # 3,000,001 - 12,000,000 → 18%
        (25000000, 0.21),        # 12,000,001 - 25,000,000 → 21%
        (50000000, 0.23),        # 25,000,001 - 50,000,000 → 23%
        (float('inf'), 0.25),    # Above 50,000,000 → 25%
    ]
    
    # Subscription Plans
    FREE_PLAN_LIMIT: int = 100  # Max transactions for free plan
    BASIC_PLAN_PRICE: float = 2500.0  # ₦2,500/month
    PREMIUM_PLAN_PRICE: float = 5000.0  # ₦5,000/month
    ENTERPRISE_PLAN_PRICE: float = 15000.0  # ₦15,000/month
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()


def ensure_upload_dir():
    """Ensure upload directory exists"""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "statements"), exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "exports"), exist_ok=True)
