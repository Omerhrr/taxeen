"""
Bank Statement Parsers Package
Parses PDF bank statements from various Nigerian banks
"""

from .statement_parser import (
    StatementParser,
    parse_bank_statement,
    detect_bank,
    SUPPORTED_BANKS
)

__all__ = [
    'StatementParser',
    'parse_bank_statement',
    'detect_bank',
    'SUPPORTED_BANKS'
]
