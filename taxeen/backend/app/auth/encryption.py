"""
Encryption Module
AES-256 encryption for sensitive data (NIN, etc.)
"""

import base64
import os
import hashlib
from typing import Optional, Tuple
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from app.config import settings


def get_aes_key() -> bytes:
    """
    Derive a 32-byte AES-256 key from the secret key
    
    Returns:
        32-byte key for AES-256 encryption
    """
    # Use SHA-256 to derive a 32-byte key from the secret
    key = hashlib.sha256(settings.AES_SECRET_KEY.encode()).digest()
    return key


def encrypt_nin(nin: str) -> Tuple[str, str]:
    """
    Encrypt a Nigerian National Identity Number (NIN) using AES-256-CBC
    
    Args:
        nin: Plain text NIN (11 digits)
        
    Returns:
        Tuple of (encrypted_nin_base64, iv_base64)
    """
    if not nin:
        return None, None
    
    # Validate NIN format (11 digits)
    if not nin.isdigit() or len(nin) != 11:
        raise ValueError("NIN must be exactly 11 digits")
    
    # Get the encryption key
    key = get_aes_key()
    
    # Generate a random 16-byte IV (initialization vector)
    iv = os.urandom(16)
    
    # Pad the plaintext to a multiple of 16 bytes (AES block size)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(nin.encode()) + padder.finalize()
    
    # Create the cipher and encrypt
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return as base64 strings for storage
    encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')
    iv_b64 = base64.b64encode(iv).decode('utf-8')
    
    return encrypted_b64, iv_b64


def decrypt_nin(encrypted_nin: str, iv: str) -> str:
    """
    Decrypt a NIN using AES-256-CBC
    
    Args:
        encrypted_nin: Base64 encoded encrypted NIN
        iv: Base64 encoded initialization vector
        
    Returns:
        Plain text NIN (11 digits)
    """
    if not encrypted_nin or not iv:
        return None
    
    # Get the encryption key
    key = get_aes_key()
    
    # Decode from base64
    encrypted_data = base64.b64decode(encrypted_nin)
    iv_bytes = base64.b64decode(iv)
    
    # Create the cipher and decrypt
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv_bytes), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(padded_data) + unpadder.finalize()
    
    return decrypted.decode('utf-8')


def encrypt_data(plaintext: str) -> Tuple[str, str]:
    """
    Encrypt arbitrary data using AES-256-CBC
    
    Args:
        plaintext: Plain text to encrypt
        
    Returns:
        Tuple of (encrypted_data_base64, iv_base64)
    """
    if not plaintext:
        return None, None
    
    # Get the encryption key
    key = get_aes_key()
    
    # Generate a random 16-byte IV
    iv = os.urandom(16)
    
    # Pad the plaintext
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    
    # Encrypt
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return as base64
    encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')
    iv_b64 = base64.b64encode(iv).decode('utf-8')
    
    return encrypted_b64, iv_b64


def decrypt_data(encrypted_data: str, iv: str) -> str:
    """
    Decrypt data using AES-256-CBC
    
    Args:
        encrypted_data: Base64 encoded encrypted data
        iv: Base64 encoded initialization vector
        
    Returns:
        Plain text data
    """
    if not encrypted_data or not iv:
        return None
    
    # Get the encryption key
    key = get_aes_key()
    
    # Decode from base64
    encrypted_bytes = base64.b64decode(encrypted_data)
    iv_bytes = base64.b64decode(iv)
    
    # Decrypt
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv_bytes), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_bytes) + decryptor.finalize()
    
    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(padded_data) + unpadder.finalize()
    
    return decrypted.decode('utf-8')


def hash_data(data: str) -> str:
    """
    Create a SHA-256 hash of data (one-way, for verification purposes)
    
    Args:
        data: Data to hash
        
    Returns:
        Hexadecimal hash string
    """
    return hashlib.sha256(data.encode()).hexdigest()


def verify_hash(data: str, hash_value: str) -> bool:
    """
    Verify data against a SHA-256 hash
    
    Args:
        data: Plain text data to verify
        hash_value: Expected hash value
        
    Returns:
        True if data matches hash, False otherwise
    """
    return hash_data(data) == hash_value


class EncryptionService:
    """Service class for encryption operations"""
    
    def __init__(self, key: Optional[bytes] = None):
        """
        Initialize encryption service
        
        Args:
            key: Optional custom key (uses default if not provided)
        """
        self.key = key or get_aes_key()
    
    def encrypt(self, plaintext: str) -> Tuple[str, str]:
        """Encrypt data and return (encrypted_b64, iv_b64)"""
        return encrypt_data(plaintext)
    
    def decrypt(self, encrypted: str, iv: str) -> str:
        """Decrypt data"""
        return decrypt_data(encrypted, iv)
    
    def encrypt_nin(self, nin: str) -> Tuple[str, str]:
        """Encrypt NIN specifically"""
        return encrypt_nin(nin)
    
    def decrypt_nin(self, encrypted_nin: str, iv: str) -> str:
        """Decrypt NIN specifically"""
        return decrypt_nin(encrypted_nin, iv)
