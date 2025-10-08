from typing import Any, Dict
from .base import DomainEvent


class TransactionCreated(DomainEvent):
    """Event raised when a transaction is created."""

    def __init__(
        self,
        transaction_id: str,
        user_id: str,
        transaction_type: str,
        amount: str,
        category_id: str,
        transaction_date: str,
    ):
        event_data = {
            "transaction_id": transaction_id,
            "user_id": user_id,
            "transaction_type": transaction_type,
            "amount": amount,
            "category_id": category_id,
            "transaction_date": transaction_date,
        }
        super().__init__(event_data)


class TransactionUpdated(DomainEvent):
    """Event raised when a transaction is updated."""

    def __init__(
        self,
        transaction_id: str,
        user_id: str,
        updated_fields: Dict[str, Any],
    ):
        event_data = {
            "transaction_id": transaction_id,
            "user_id": user_id,
            "updated_fields": updated_fields,
        }
        super().__init__(event_data)


class TransactionDeleted(DomainEvent):
    """Event raised when a transaction is deleted."""

    def __init__(
        self,
        transaction_id: str,
        user_id: str,
        transaction_type: str,
        amount: str,
    ):
        event_data = {
            "transaction_id": transaction_id,
            "user_id": user_id,
            "transaction_type": transaction_type,
            "amount": amount,
        }
        super().__init__(event_data)
