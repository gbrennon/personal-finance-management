"""
Finance domain events.
"""

from typing import Dict, Any
from foundations.domain.aggregate_root import DomainEvent


class TransactionCreated(DomainEvent):
    """
    Event raised when a new transaction is created.
    """

    def __init__(
        self,
        aggregate_id: str,
        user_id: str,
        transaction_type: str,
        amount: float,
        category_id: str,
        transaction_date: str,
    ):
        super().__init__(
            aggregate_id=aggregate_id,
            event_type="TransactionCreated",
            data={
                "user_id": user_id,
                "transaction_type": transaction_type,
                "amount": amount,
                "category_id": category_id,
                "transaction_date": transaction_date,
            },
        )


class BudgetCreated(DomainEvent):
    """
    Event raised when a new budget is created.
    """

    def __init__(
        self, aggregate_id: str, user_id: str, amount: float, month: int, year: int
    ):
        super().__init__(
            aggregate_id=aggregate_id,
            event_type="BudgetCreated",
            data={"user_id": user_id, "amount": amount, "month": month, "year": year},
        )


class BudgetExceeded(DomainEvent):
    """
    Event raised when a budget is exceeded.
    """

    def __init__(
        self,
        aggregate_id: str,
        user_id: str,
        budget_amount: float,
        actual_amount: float,
        month: int,
        year: int,
    ):
        super().__init__(
            aggregate_id=aggregate_id,
            event_type="BudgetExceeded",
            data={
                "user_id": user_id,
                "budget_amount": budget_amount,
                "actual_amount": actual_amount,
                "month": month,
                "year": year,
            },
        )
