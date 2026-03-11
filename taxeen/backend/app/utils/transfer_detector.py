"""
Internal Transfer Detector
Detects internal transfers between user's own bank accounts
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class TransactionMatch:
    """Represents a matched pair of internal transfer transactions"""
    debit_transaction_id: int
    credit_transaction_id: int
    amount: Decimal
    debit_bank_id: int
    credit_bank_id: int
    confidence_score: float


class InternalTransferDetector:
    """
    Detects internal transfers between a user's bank accounts

    Internal transfers should not be counted as income for tax purposes.
    This detector matches debit and credit transactions that are likely
    transfers between the same user's accounts.
    """

    # Configuration
    DEFAULT_DATE_TOLERANCE_DAYS = 3
    DEFAULT_AMOUNT_TOLERANCE_PERCENT = 0.01  # 1% tolerance for amount differences

    def __init__(
        self,
        date_tolerance_days: int = DEFAULT_DATE_TOLERANCE_DAYS,
        amount_tolerance_percent: float = DEFAULT_AMOUNT_TOLERANCE_PERCENT
    ):
        self.date_tolerance = timedelta(days=date_tolerance_days)
        self.amount_tolerance = amount_tolerance_percent

    def calculate_similarity_score(
        self,
        debit: Dict,
        credit: Dict
    ) -> float:
        """
        Calculate similarity score between debit and credit transactions

        Returns a score between 0 and 1, where 1 is a perfect match
        """
        score = 0.0
        factors = 0

        # Amount comparison (most important factor)
        debit_amount = Decimal(str(debit.get('amount', 0)))
        credit_amount = Decimal(str(credit.get('amount', 0)))

        if debit_amount > 0 and credit_amount > 0:
            # Allow small differences (bank fees, etc.)
            diff_percent = abs(debit_amount - credit_amount) / max(debit_amount, credit_amount)
            if diff_percent <= self.amount_tolerance:
                score += 1.0 - diff_percent
            factors += 1

        # Date comparison
        try:
            debit_date = datetime.fromisoformat(debit.get('date', '').replace('Z', '+00:00'))
            credit_date = datetime.fromisoformat(credit.get('date', '').replace('Z', '+00:00'))
            date_diff = abs((debit_date - credit_date).days)

            if date_diff <= self.date_tolerance.days:
                date_score = 1.0 - (date_diff / (self.date_tolerance.days + 1))
                score += date_score
            factors += 1
        except (ValueError, TypeError):
            pass

        # Different bank accounts check
        debit_bank = debit.get('bank_account_id')
        credit_bank = credit.get('bank_account_id')
        if debit_bank and credit_bank and debit_bank != credit_bank:
            score += 1.0
            factors += 1

        # Description analysis
        debit_desc = debit.get('description', '').lower()
        credit_desc = credit.get('description', '').lower()

        # Check for transfer keywords
        transfer_keywords = ['transfer', 'tfr', 'trf', 'xfer', 'own account']
        debit_has_keyword = any(kw in debit_desc for kw in transfer_keywords)
        credit_has_keyword = any(kw in credit_desc for kw in transfer_keywords)

        if debit_has_keyword or credit_has_keyword:
            score += 0.5
        factors += 1

        return score / factors if factors > 0 else 0.0

    def detect(
        self,
        transactions: List[Dict],
        user_bank_accounts: List[int]
    ) -> Tuple[List[Dict], List[TransactionMatch]]:
        """
        Detect internal transfers in a list of transactions

        Args:
            transactions: List of transaction dictionaries
            user_bank_accounts: List of user's bank account IDs

        Returns:
            Tuple of (updated transactions with is_internal_transfer flag, list of matches)
        """
        # Separate debits and credits
        debits = [t for t in transactions if t.get('direction') == 'debit']
        credits = [t for t in transactions if t.get('direction') == 'credit']

        matches = []
        matched_debit_ids = set()
        matched_credit_ids = set()

        # Compare each debit with each credit
        for debit in debits:
            if debit.get('id') in matched_debit_ids:
                continue

            best_match = None
            best_score = 0.5  # Minimum threshold

            for credit in credits:
                if credit.get('id') in matched_credit_ids:
                    continue

                # Must be different bank accounts
                if debit.get('bank_account_id') == credit.get('bank_account_id'):
                    continue

                # Must be user's accounts
                if (debit.get('bank_account_id') not in user_bank_accounts or
                    credit.get('bank_account_id') not in user_bank_accounts):
                    continue

                score = self.calculate_similarity_score(debit, credit)

                if score > best_score:
                    best_score = score
                    best_match = credit

            if best_match:
                matches.append(TransactionMatch(
                    debit_transaction_id=debit['id'],
                    credit_transaction_id=best_match['id'],
                    amount=Decimal(str(debit.get('amount', 0))),
                    debit_bank_id=debit.get('bank_account_id'),
                    credit_bank_id=best_match.get('bank_account_id'),
                    confidence_score=best_score
                ))
                matched_debit_ids.add(debit['id'])
                matched_credit_ids.add(best_match['id'])

        # Mark transactions as internal transfers
        updated_transactions = []
        for t in transactions:
            t_copy = t.copy()
            if t['id'] in matched_debit_ids or t['id'] in matched_credit_ids:
                t_copy['is_internal_transfer'] = True
                t_copy['taxable'] = False
            else:
                t_copy['is_internal_transfer'] = t.get('is_internal_transfer', False)
                t_copy['taxable'] = t.get('taxable', True)
            updated_transactions.append(t_copy)

        return updated_transactions, matches


def detect_internal_transfers(
    transactions: List[Dict],
    user_bank_accounts: List[int]
) -> Tuple[List[Dict], List[TransactionMatch]]:
    """
    Convenience function to detect internal transfers

    Args:
        transactions: List of transaction dictionaries
        user_bank_accounts: List of user's bank account IDs

    Returns:
        Tuple of (updated transactions, list of matches)
    """
    detector = InternalTransferDetector()
    return detector.detect(transactions, user_bank_accounts)


if __name__ == "__main__":
    # Test the detector
    test_transactions = [
        {"id": 1, "date": "2026-01-15", "amount": 50000, "direction": "debit", "bank_account_id": 1, "description": "Transfer to GTBank"},
        {"id": 2, "date": "2026-01-15", "amount": 50000, "direction": "credit", "bank_account_id": 2, "description": "Transfer from Access"},
        {"id": 3, "date": "2026-01-16", "amount": 25000, "direction": "debit", "bank_account_id": 1, "description": "POS Purchase"},
        {"id": 4, "date": "2026-01-17", "amount": 150000, "direction": "credit", "bank_account_id": 1, "description": "Salary"},
    ]

    user_banks = [1, 2]

    updated, matches = detect_internal_transfers(test_transactions, user_banks)

    print("Internal Transfer Matches:")
    for m in matches:
        print(f"  Debit #{m.debit_transaction_id} <-> Credit #{m.credit_transaction_id}: ₦{m.amount:,.2f} (confidence: {m.confidence_score:.2f})")

    print("\nUpdated Transactions:")
    for t in updated:
        print(f"  #{t['id']}: {t['direction']} ₦{t['amount']:,.2f} - Internal Transfer: {t['is_internal_transfer']}")
