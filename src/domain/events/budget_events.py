from typing import Any, Dict, Optional
from .base import DomainEvent


class BudgetCreated(DomainEvent):
    """Event raised when a budget is created."""

    def __init__(
        self,
        budget_id: str,
        user_id: str,
        month: int,
        year: int,
        amount: Optional[str] = None,
    ):
        event_data = {
            "budget_id": budget_id,
            "user_id": user_id,
            "month": month,
            "year": year,
            "amount": amount,
        }
        super().__init__(event_data)


class BudgetUpdated(DomainEvent):
    """Event raised when a budget is updated."""

    def __init__(
        self,
        budget_id: str,
        user_id: str,
        updated_fields: Dict[str, Any],
    ):
        event_data = {
            "budget_id": budget_id,
            "user_id": user_id,
            "updated_fields": updated_fields,
        }
        super().__init__(event_data)


class BudgetExceeded(DomainEvent):
    """Event raised when a budget is exceeded."""

    def __init__(
        self,
        budget_id: str,
        user_id: str,
        month: int,
        year: int,
        budget_amount: str,
        spent_amount: str,
        excess_amount: str,
    ):
        event_data = {
            "budget_id": budget_id,
            "user_id": user_id,
            "month": month,
            "year": year,
            "budget_amount": budget_amount,
            "spent_amount": spent_amount,
            "excess_amount": excess_amount,
        }
        super().__init__(event_data)
