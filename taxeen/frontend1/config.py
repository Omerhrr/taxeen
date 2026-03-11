"""
Taxeen Frontend Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'taxeen-secret-key-change-in-production')
    
    # API Configuration
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000/api')
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))
    
    # Session Configuration
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'false').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    
    # Flask Configuration
    DEBUG = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    TESTING = os.getenv('FLASK_TESTING', 'false').lower() == 'true'
    
    # Template Configuration
    TEMPLATES_AUTO_RELOAD = True
    
    # Static files
    STATIC_FOLDER = 'static'
    STATIC_URL_PATH = '/static'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    
    # Production security settings
    SESSION_COOKIE_SAMESITE = 'Strict'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
