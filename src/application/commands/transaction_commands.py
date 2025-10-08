from dataclasses import dataclass
from datetime import date
from typing import Optional
from decimal import Decimal


@dataclass
class CreateTransactionCommand:
    """Command to create a new transaction."""

    user_id: str
    transaction_type: str  # "Income" or "Expense"
    amount: Decimal
    category_id: str
    transaction_date: date
    description: Optional[str] = None


@dataclass
class UpdateTransactionCommand:
    """Command to update an existing transaction."""

    transaction_id: str
    user_id: str
    amount: Optional[Decimal] = None
    category_id: Optional[str] = None
    description: Optional[str] = None


@dataclass
class DeleteTransactionCommand:
    """Command to delete a transaction."""

    transaction_id: str
    user_id: str
