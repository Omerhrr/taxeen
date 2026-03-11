"""
Bank Statement Parser
Extracts transactions from PDF bank statements from Nigerian banks
"""

import os
import re
import json
import tempfile
from typing import List, Dict, Optional, Tuple
from datetime import datetime, date
from decimal import Decimal
import logging

# PDF parsing libraries
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    import pytesseract
    from PIL import Image
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False

logger = logging.getLogger(__name__)

# Supported Nigerian banks
SUPPORTED_BANKS = [
    "GTBank", "Access Bank", "UBA", "Zenith Bank", "First Bank",
    "Stanbic IBTC", "Fidelity Bank", "Union Bank", "Ecobank",
    "Wema Bank", "Sterling Bank", "FCMB", "Kuda", "OPay", "Moniepoint", "PalmPay"
]


class Transaction:
    """Represents a single bank transaction"""

    def __init__(self, date: str, description: str, amount: Decimal,
                 direction: str, balance: Optional[Decimal] = None,
                 reference: Optional[str] = None, category: Optional[str] = None):
        self.date = date
        self.description = description
        self.amount = amount
        self.direction = direction  # 'credit' or 'debit'
        self.balance = balance
        self.reference = reference
        self.category = category

    def to_dict(self) -> Dict:
        return {
            "date": self.date,
            "description": self.description,
            "amount": float(self.amount),
            "direction": self.direction,
            "balance": float(self.balance) if self.balance else None,
            "reference": self.reference,
            "category": self.category
        }


class StatementParser:
    """Parses bank statements from PDF files"""

    DATE_PATTERNS = [
        r'(\d{2}[-/]\d{2}[-/]\d{4})',
        r'(\d{4}[-/]\d{2}[-/]\d{2})',
        r'(\d{2}[-/]\w{3}[-/]\d{4})',
    ]
    AMOUNT_PATTERN = r'[\d,]+\.?\d*'

    def __init__(self):
        self.transactions: List[Transaction] = []
        self.account_info: Dict = {}
        self.bank_name: Optional[str] = None

    def detect_bank(self, text: str) -> Optional[str]:
        text_lower = text.lower()
        bank_keywords = {
            "GTBank": ["gtbank", "guaranty trust", "gtb"],
            "Access Bank": ["access bank", "accessbank"],
            "UBA": ["united bank for africa", "uba"],
            "Zenith Bank": ["zenith bank", "zenithbank"],
            "First Bank": ["first bank", "firstbank"],
        }
        for bank, keywords in bank_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return bank
        return None

    def extract_text_from_pdf(self, file_path: str) -> str:
        if not HAS_PDFPLUMBER:
            raise ImportError("pdfplumber is required")
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def parse_date(self, date_str: str) -> Optional[str]:
        formats = ["%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%d-%b-%Y"]
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return None

    def parse_amount(self, amount_str: str) -> Optional[Decimal]:
        if not amount_str:
            return None
        cleaned = re.sub(r'[₦$£€,\s]', '', str(amount_str))
        try:
            return Decimal(cleaned)
        except Exception:
            return None

    def parse_generic_statement(self, text: str) -> List[Transaction]:
        transactions = []
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            for pattern in self.DATE_PATTERNS:
                match = re.search(pattern, line)
                if match:
                    date_str = self.parse_date(match.group(1))
                    if date_str:
                        amounts = re.findall(r'[\d,]+\.\d{2}', line)
                        if amounts:
                            amount = self.parse_amount(amounts[0])
                            direction = 'credit' if any(kw in line.lower() for kw in ['cr', 'credit', 'deposit']) else 'debit'
                            balance = self.parse_amount(amounts[-1]) if len(amounts) > 1 else None
                            description = re.sub(pattern, '', line)
                            description = re.sub(r'[\d,]+\.\d{2}', '', description).strip()[:200]
                            if amount and amount > 0:
                                transactions.append(Transaction(
                                    date=date_str, description=description,
                                    amount=amount, direction=direction, balance=balance
                                ))
                    break
        return transactions

    def parse(self, file_path: str) -> Tuple[List[Transaction], Dict]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        self.bank_name = self.detect_bank(text)
        self.transactions = self.parse_generic_statement(text)
        self.account_info = {
            "bank_name": self.bank_name,
            "account_number": self._extract_account_number(text),
        }
        return self.transactions, self.account_info

    def _extract_account_number(self, text: str) -> Optional[str]:
        match = re.search(r'\b(\d{10})\b', text)
        return match.group(1) if match else None

    def to_json(self, output_path: str) -> None:
        data = {"account_info": self.account_info, "transactions": [t.to_dict() for t in self.transactions]}
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

    def to_markdown(self, output_path: str) -> None:
        lines = [f"# Bank Statement - {self.bank_name or 'Unknown'}", "", "| Date | Description | Direction | Amount |", "|------|-------------|-----------|--------|"]
        for t in self.transactions:
            lines.append(f"| {t.date} | {t.description[:40]} | {t.direction} | ₦{t.amount:,.2f} |")
        with open(output_path, 'w') as f:
            f.write('\n'.join(lines))


def parse_bank_statement(file_path: str) -> Tuple[List[Dict], Dict]:
    parser = StatementParser()
    transactions, account_info = parser.parse(file_path)
    return [t.to_dict() for t in transactions], account_info


def detect_bank(file_path: str) -> Optional[str]:
    parser = StatementParser()
    text = parser.extract_text_from_pdf(file_path)
    return parser.detect_bank(text)
