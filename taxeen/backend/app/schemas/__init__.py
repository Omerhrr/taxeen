"""
Pydantic Schemas Package
Request/Response models for API validation
"""

from .user import (
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
    UserWithSubscription,
)
from .auth import (
    Token,
    TokenRefresh,
    LoginResponse,
    PasswordChange,
)
from .bank_account import (
    BankAccountCreate,
    BankAccountUpdate,
    BankAccountResponse,
    BankAccountList,
)
from .transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionList,
    TransactionFilter,
    TransactionClassify,
    TransactionSummary,
)
from .statement import (
    StatementUploadResponse,
    StatementList,
    StatementProcessRequest,
)
from .tax_report import (
    TaxReportRequest,
    TaxReportResponse,
    TaxReportSummary,
    DeductionItem,
    TaxBandBreakdown,
)
from .common import (
    PaginationParams,
    PaginatedResponse,
    ErrorResponse,
    SuccessResponse,
    MessageResponse,
)

__all__ = [
    # User schemas
    'UserCreate',
    'UserLogin',
    'UserResponse',
    'UserUpdate',
    'UserWithSubscription',
    
    # Auth schemas
    'Token',
    'TokenRefresh',
    'LoginResponse',
    'PasswordChange',
    
    # Bank Account schemas
    'BankAccountCreate',
    'BankAccountUpdate',
    'BankAccountResponse',
    'BankAccountList',
    
    # Transaction schemas
    'TransactionCreate',
    'TransactionUpdate',
    'TransactionResponse',
    'TransactionList',
    'TransactionFilter',
    'TransactionClassify',
    'TransactionSummary',
    
    # Statement schemas
    'StatementUploadResponse',
    'StatementList',
    'StatementProcessRequest',
    
    # Tax Report schemas
    'TaxReportRequest',
    'TaxReportResponse',
    'TaxReportSummary',
    'DeductionItem',
    'TaxBandBreakdown',
    
    # Common schemas
    'PaginationParams',
    'PaginatedResponse',
    'ErrorResponse',
    'SuccessResponse',
    'MessageResponse',
]
