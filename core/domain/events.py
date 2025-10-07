from typing import Any, Dict
from datetime import datetime
from .messages import Message


class Event(Message):
    """Base class for all events in the system"""

    def __init__(self, event_type: str, data: Dict[str, Any], **kwargs):
        super().__init__(**kwargs)
        self.event_type = event_type
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type,
            "data": self.data,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        return cls(
            event_type=data["event_type"],
            data=data["data"],
            message_id=data["message_id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


class EventPublisher:
    """Publishes events to the message bus"""

    def __init__(self, message_dispatcher):
        self.message_dispatcher = message_dispatcher

    async def publish(self, event: Event) -> None:
        """Publish an event to the message bus"""
        await self.message_dispatcher.dispatch(event)


# Domain Events
class TransactionCreatedEvent(Event):
    def __init__(
        self,
        transaction_id: str,
        user_id: str,
        transaction_type: str,
        amount: float,
        category: str,
        date: str,
        **kwargs,
    ):
        super().__init__(
            event_type="transaction_created",
            data={
                "transaction_id": transaction_id,
                "user_id": user_id,
                "transaction_type": transaction_type,
                "amount": amount,
                "category": category,
                "date": date,
            },
            **kwargs,
        )


class BudgetExceededEvent(Event):
    def __init__(
        self,
        user_id: str,
        month: int,
        year: int,
        budget_amount: float,
        actual_amount: float,
        **kwargs,
    ):
        super().__init__(
            event_type="budget_exceeded",
            data={
                "user_id": user_id,
                "month": month,
                "year": year,
                "budget_amount": budget_amount,
                "actual_amount": actual_amount,
            },
            **kwargs,
        )


class InvoiceCreatedEvent(Event):
    def __init__(
        self,
        invoice_id: str,
        user_id: str,
        client_name: str,
        amount: float,
        due_date: str,
        **kwargs,
    ):
        super().__init__(
            event_type="invoice_created",
            data={
                "invoice_id": invoice_id,
                "user_id": user_id,
                "client_name": client_name,
                "amount": amount,
                "due_date": due_date,
            },
            **kwargs,
        )


class InvestmentCreatedEvent(Event):
    def __init__(
        self,
        investment_id: str,
        user_id: str,
        investment_type: str,
        amount: float,
        expected_return: float,
        **kwargs,
    ):
        super().__init__(
            event_type="investment_created",
            data={
                "investment_id": investment_id,
                "user_id": user_id,
                "investment_type": investment_type,
                "amount": amount,
                "expected_return": expected_return,
            },
            **kwargs,
        )


class RetirementPlanCreatedEvent(Event):
    def __init__(
        self,
        plan_id: str,
        user_id: str,
        target_amount: float,
        target_age: int,
        monthly_contribution: float,
        **kwargs,
    ):
        super().__init__(
            event_type="retirement_plan_created",
            data={
                "plan_id": plan_id,
                "user_id": user_id,
                "target_amount": target_amount,
                "target_age": target_age,
                "monthly_contribution": monthly_contribution,
            },
            **kwargs,
        )
