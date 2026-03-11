# API package
from .auth import router as auth_router
from .bank_accounts import router as bank_accounts_router
from .transactions import router as transactions_router
from .uploads import router as uploads_router
from .tax_reports import router as tax_reports_router
from .admin import router as admin_router

__all__ = [
    'auth_router',
    'bank_accounts_router',
    'transactions_router',
    'uploads_router',
    'tax_reports_router',
    'admin_router'
]
