from typing import Any, Dict
from .base import DomainEvent


class InvestmentCreated(DomainEvent):
    """Event raised when an investment is created."""

    def __init__(
        self,
        investment_id: str,
        user_id: str,
        investment_type: str,
        symbol: str,
        name: str,
        initial_amount: str,
        purchase_date: str,
    ):
        event_data = {
            "investment_id": investment_id,
            "user_id": user_id,
            "investment_type": investment_type,
            "symbol": symbol,
            "name": name,
            "initial_amount": initial_amount,
            "purchase_date": purchase_date,
        }
        super().__init__(event_data)


class InvestmentValueUpdated(DomainEvent):
    """Event raised when an investment value is updated."""

    def __init__(
        self,
        investment_id: str,
        user_id: str,
        symbol: str,
        old_value: str,
        new_value: str,
        gain_loss_amount: str,
        gain_loss_percentage: float,
    ):
        event_data = {
            "investment_id": investment_id,
            "user_id": user_id,
            "symbol": symbol,
            "old_value": old_value,
            "new_value": new_value,
            "gain_loss_amount": gain_loss_amount,
            "gain_loss_percentage": gain_loss_percentage,
        }
        super().__init__(event_data)
