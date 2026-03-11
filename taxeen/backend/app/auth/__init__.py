"""
Authentication Package
Password hashing, JWT tokens, and encryption
"""

from .security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
    get_current_user,
    get_current_admin_user,
    require_active_subscription,
    TokenData,
)
from .encryption import (
    encrypt_nin,
    decrypt_nin,
    encrypt_data,
    decrypt_data,
    hash_data,
    verify_hash,
    EncryptionService,
)

__all__ = [
    # Password hashing
    'hash_password',
    'verify_password',
    
    # JWT tokens
    'create_access_token',
    'create_refresh_token',
    'verify_token',
    
    # Auth dependencies
    'get_current_user',
    'get_current_admin_user',
    'require_active_subscription',
    'TokenData',
    
    # NIN Encryption (AES-256)
    'encrypt_nin',
    'decrypt_nin',
    
    # General encryption
    'encrypt_data',
    'decrypt_data',
    'hash_data',
    'verify_hash',
    'EncryptionService',
]
