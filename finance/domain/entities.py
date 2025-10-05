"""
Finance domain entities.
"""

from decimal import Decimal
from datetime import date
from typing import Optional, Dict, Any
from enum import Enum

from foundations import Entity, AggregateRoot
from .events import TransactionCreated, BudgetExceeded, BudgetCreated


class TransactionType(Enum):
    INCOME = "Income"
    EXPENSE = "Expense"


class Category(Entity):
    """
    Category entity for organizing transactions.
    """

    def __init__(
        self,
        name: str,
        transaction_type: TransactionType,
        user_id: str,
        entity_id: Optional[str] = None,
    ):
        super().__init__(entity_id)
        self.name = name
        self.transaction_type = transaction_type
        self.user_id = user_id

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update(
            {
                "name": self.name,
                "transaction_type": self.transaction_type.value,
                "user_id": self.user_id,
            }
        )
        return base_dict


class FinanceTransaction(AggregateRoot):
    """
    Finance transaction aggregate root.
    """

    def __init__(
        self,
        user_id: str,
        transaction_type: TransactionType,
        amount: Decimal,
        category: Category,
        transaction_date: date,
        entity_id: Optional[str] = None,
    ):
        super().__init__(entity_id)
        self.user_id = user_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.category = category
        self.transaction_date = transaction_date

        # Add domain event
        self._add_domain_event(
            TransactionCreated(
                aggregate_id=self.id,
                user_id=user_id,
                transaction_type=transaction_type.value,
                amount=float(amount),
                category_id=category.id,
                transaction_date=transaction_date.isoformat(),
            )
        )

    def update_amount(self, new_amount: Decimal) -> None:
        """Update the transaction amount."""
        if new_amount <= 0:
            raise ValueError("Transaction amount must be positive")

        self.amount = new_amount
        self._update_timestamp()

    def update_category(self, new_category: Category) -> None:
        """Update the transaction category."""
        if new_category.transaction_type != self.transaction_type:
            raise ValueError("Category type must match transaction type")

        self.category = new_category
        self._update_timestamp()

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update(
            {
                "user_id": self.user_id,
                "transaction_type": self.transaction_type.value,
                "amount": float(self.amount),
                "category": self.category.to_dict(),
                "transaction_date": self.transaction_date.isoformat(),
            }
        )
        return base_dict


class Budget(AggregateRoot):
    """
    Budget aggregate root.
    """

    def __init__(
        self,
        user_id: str,
        amount: Optional[Decimal],
        month: int,
        year: int,
        entity_id: Optional[str] = None,
    ):
        super().__init__(entity_id)
        self.user_id = user_id
        self.amount = amount
        self.month = month
        self.year = year

        if amount is not None:
            # Add domain event
            self._add_domain_event(
                BudgetCreated(
                    aggregate_id=self.id,
                    user_id=user_id,
                    amount=float(amount),
                    month=month,
                    year=year,
                )
            )

    def update_amount(self, new_amount: Optional[Decimal]) -> None:
        """Update the budget amount."""
        if new_amount is not None and new_amount <= 0:
            raise ValueError("Budget amount must be positive")

        self.amount = new_amount
        self._update_timestamp()

    def check_budget_exceeded(self, total_expenses: Decimal) -> None:
        """Check if budget is exceeded and emit event if so."""
        if self.amount is not None and total_expenses > self.amount:
            self._add_domain_event(
                BudgetExceeded(
                    aggregate_id=self.id,
                    user_id=self.user_id,
                    budget_amount=float(self.amount),
                    actual_amount=float(total_expenses),
                    month=self.month,
                    year=self.year,
                )
            )

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update(
            {
                "user_id": self.user_id,
                "amount": float(self.amount) if self.amount else None,
                "month": self.month,
                "year": self.year,
            }
        )
        return base_dict
