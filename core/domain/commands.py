from typing import Any, Dict
from datetime import datetime
from .messages import Message


class Command(Message):
    """Base class for all commands in the system"""

    def __init__(self, command_type: str, data: Dict[str, Any], **kwargs):
        super().__init__(**kwargs)
        self.command_type = command_type
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "timestamp": self.timestamp.isoformat(),
            "command_type": self.command_type,
            "data": self.data,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Command":
        return cls(
            command_type=data["command_type"],
            data=data["data"],
            message_id=data["message_id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


class CommandDispatcher:
    """Dispatches commands to the message bus"""

    def __init__(self, message_dispatcher):
        self.message_dispatcher = message_dispatcher

    async def dispatch(self, command: Command) -> None:
        """Dispatch a command to the message bus"""
        await self.message_dispatcher.dispatch(command)


# Domain Commands
class CreateTransactionCommand(Command):
    def __init__(
        self,
        user_id: str,
        transaction_type: str,
        amount: float,
        category: str,
        date: str,
        **kwargs,
    ):
        super().__init__(
            command_type="create_transaction",
            data={
                "user_id": user_id,
                "transaction_type": transaction_type,
                "amount": amount,
                "category": category,
                "date": date,
            },
            **kwargs,
        )


class UpdateTransactionCommand(Command):
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
            command_type="update_transaction",
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


class DeleteTransactionCommand(Command):
    def __init__(self, transaction_id: str, user_id: str, **kwargs):
        super().__init__(
            command_type="delete_transaction",
            data={"transaction_id": transaction_id, "user_id": user_id},
            **kwargs,
        )


class CreateBudgetCommand(Command):
    def __init__(self, user_id: str, amount: float, month: int, year: int, **kwargs):
        super().__init__(
            command_type="create_budget",
            data={"user_id": user_id, "amount": amount, "month": month, "year": year},
            **kwargs,
        )


class CreateInvoiceCommand(Command):
    def __init__(
        self,
        user_id: str,
        client_name: str,
        amount: float,
        due_date: str,
        description: str = "",
        **kwargs,
    ):
        super().__init__(
            command_type="create_invoice",
            data={
                "user_id": user_id,
                "client_name": client_name,
                "amount": amount,
                "due_date": due_date,
                "description": description,
            },
            **kwargs,
        )


class CreateInvestmentCommand(Command):
    def __init__(
        self,
        user_id: str,
        investment_type: str,
        amount: float,
        expected_return: float,
        risk_level: str = "medium",
        **kwargs,
    ):
        super().__init__(
            command_type="create_investment",
            data={
                "user_id": user_id,
                "investment_type": investment_type,
                "amount": amount,
                "expected_return": expected_return,
                "risk_level": risk_level,
            },
            **kwargs,
        )


class CreateRetirementPlanCommand(Command):
    def __init__(
        self,
        user_id: str,
        target_amount: float,
        target_age: int,
        monthly_contribution: float,
        current_age: int,
        **kwargs,
    ):
        super().__init__(
            command_type="create_retirement_plan",
            data={
                "user_id": user_id,
                "target_amount": target_amount,
                "target_age": target_age,
                "monthly_contribution": monthly_contribution,
                "current_age": current_age,
            },
            **kwargs,
        )


class GenerateForecastCommand(Command):
    def __init__(self, user_id: str, forecast_months: int = 3, **kwargs):
        super().__init__(
            command_type="generate_forecast",
            data={"user_id": user_id, "forecast_months": forecast_months},
            **kwargs,
        )
