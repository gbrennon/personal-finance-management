from datetime import date
from enum import Enum
from typing import Optional

from ..value_objects.money import Money
from ..value_objects.transaction_id import TransactionId
from ..value_objects.user_id import UserId
from ..value_objects.category_id import CategoryId


class TransactionType(Enum):
    INCOME = "Income"
    EXPENSE = "Expense"


class Transaction:
    """Domain entity representing a financial transaction."""

    def __init__(
        self,
        transaction_id: TransactionId,
        user_id: UserId,
        transaction_type: TransactionType,
        amount: Money,
        category_id: CategoryId,
        transaction_date: date,
        description: Optional[str] = None,
    ):
        self._transaction_id = transaction_id
        self._user_id = user_id
        self._transaction_type = transaction_type
        self._amount = amount
        self._category_id = category_id
        self._transaction_date = transaction_date
        self._description = description

    @property
    def transaction_id(self) -> TransactionId:
        return self._transaction_id

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def transaction_type(self) -> TransactionType:
        return self._transaction_type

    @property
    def amount(self) -> Money:
        return self._amount

    @property
    def category_id(self) -> CategoryId:
        return self._category_id

    @property
    def transaction_date(self) -> date:
        return self._transaction_date

    @property
    def description(self) -> Optional[str]:
        return self._description

    def update_amount(self, new_amount: Money) -> None:
        """Update the transaction amount."""
        if new_amount.amount <= 0:
            raise ValueError("Transaction amount must be positive")
        self._amount = new_amount

    def update_description(self, description: Optional[str]) -> None:
        """Update the transaction description."""
        self._description = description

    def update_category(self, category_id: CategoryId) -> None:
        """Update the transaction category."""
        self._category_id = category_id

    def is_income(self) -> bool:
        """Check if this is an income transaction."""
        return self._transaction_type == TransactionType.INCOME

    def is_expense(self) -> bool:
        """Check if this is an expense transaction."""
        return self._transaction_type == TransactionType.EXPENSE

    def __eq__(self, other) -> bool:
        if not isinstance(other, Transaction):
            return False
        return self._transaction_id == other._transaction_id

    def __hash__(self) -> int:
        return hash(self._transaction_id)

    def __str__(self) -> str:
        return f"Transaction({self._transaction_id}, {self._transaction_type.value}, {self._amount})"
