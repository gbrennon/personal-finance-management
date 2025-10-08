from typing import List, Optional
import uuid

from ...domain.entities.investment import Investment, InvestmentType
from ...domain.value_objects.money import Money
from ...domain.value_objects.investment_id import InvestmentId
from ...domain.value_objects.user_id import UserId
from ...domain.events.investment_events import (
    InvestmentCreated,
    InvestmentValueUpdated,
)
from ...domain.repositories.unit_of_work import UnitOfWork
from ..commands.investment_commands import (
    CreateInvestmentCommand,
    UpdateInvestmentValueCommand,
)


class InvestmentService:
    """Application service for investment operations."""

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def create_investment(self, command: CreateInvestmentCommand) -> str:
        """Create a new investment."""
        with self._uow:
            investment_id = InvestmentId(str(uuid.uuid4()))

            # Convert string to enum
            investment_type = InvestmentType(command.investment_type)

            investment = Investment(
                investment_id=investment_id,
                user_id=UserId(command.user_id),
                investment_type=investment_type,
                symbol=command.symbol,
                name=command.name,
                initial_amount=Money(command.initial_amount),
                purchase_date=command.purchase_date,
                description=command.description,
            )

            self._uow.investments.save(investment)

            # Add domain event
            event = InvestmentCreated(
                investment_id=investment_id.value,
                user_id=command.user_id,
                investment_type=command.investment_type,
                symbol=command.symbol,
                name=command.name,
                initial_amount=str(command.initial_amount),
                purchase_date=command.purchase_date.isoformat(),
            )
            self._uow.add_event(event)

            return investment_id.value

    def update_investment_value(self, command: UpdateInvestmentValueCommand) -> None:
        """Update an investment's current value."""
        with self._uow:
            investment = self._uow.investments.get_by_id(
                InvestmentId(command.investment_id)
            )
            if not investment:
                raise ValueError("Investment not found")
            if investment.user_id.value != command.user_id:
                raise ValueError("Investment does not belong to user")

            old_value = investment.current_value
            investment.update_current_value(Money(command.new_value))

            self._uow.investments.save(investment)

            # Add domain event
            event = InvestmentValueUpdated(
                investment_id=command.investment_id,
                user_id=command.user_id,
                symbol=investment.symbol,
                old_value=str(old_value.amount),
                new_value=str(command.new_value),
                gain_loss_amount=str(investment.gain_loss_amount().amount),
                gain_loss_percentage=investment.gain_loss_percentage(),
            )
            self._uow.add_event(event)

    def get_user_investments(self, user_id: str) -> List[Investment]:
        """Get all investments for a user."""
        return self._uow.investments.get_by_user_id(UserId(user_id))

    def get_investment_by_id(
        self, investment_id: str, user_id: str
    ) -> Optional[Investment]:
        """Get an investment by ID, ensuring it belongs to the user."""
        investment = self._uow.investments.get_by_id(InvestmentId(investment_id))
        if investment and investment.user_id.value == user_id:
            return investment
        return None

    def get_investments_by_type(
        self, user_id: str, investment_type: str
    ) -> List[Investment]:
        """Get all investments for a user by type."""
        investment_type_enum = InvestmentType(investment_type)
        return self._uow.investments.get_by_user_and_type(
            UserId(user_id), investment_type_enum
        )

    def get_portfolio_summary(self, user_id: str) -> dict:
        """Get a summary of the user's investment portfolio."""
        investments = self.get_user_investments(user_id)

        if not investments:
            return {
                "total_investments": 0,
                "total_initial_value": 0,
                "total_current_value": 0,
                "total_gain_loss": 0,
                "total_gain_loss_percentage": 0.0,
                "profitable_investments": 0,
                "loss_investments": 0,
                "by_type": {},
            }

        total_initial = sum(inv.initial_amount.amount for inv in investments)
        total_current = sum(inv.current_value.amount for inv in investments)
        total_gain_loss = total_current - total_initial
        total_gain_loss_percentage = (
            float(total_gain_loss / total_initial * 100) if total_initial > 0 else 0.0
        )

        profitable_count = sum(1 for inv in investments if inv.is_profitable())
        loss_count = sum(1 for inv in investments if inv.is_loss())

        # Group by investment type
        by_type = {}
        for investment in investments:
            inv_type = investment.investment_type.value
            if inv_type not in by_type:
                by_type[inv_type] = {
                    "count": 0,
                    "initial_value": 0,
                    "current_value": 0,
                    "gain_loss": 0,
                }

            by_type[inv_type]["count"] += 1
            by_type[inv_type]["initial_value"] += float(
                investment.initial_amount.amount
            )
            by_type[inv_type]["current_value"] += float(investment.current_value.amount)
            by_type[inv_type]["gain_loss"] += float(
                investment.gain_loss_amount().amount
            )

        return {
            "total_investments": len(investments),
            "total_initial_value": float(total_initial),
            "total_current_value": float(total_current),
            "total_gain_loss": float(total_gain_loss),
            "total_gain_loss_percentage": total_gain_loss_percentage,
            "profitable_investments": profitable_count,
            "loss_investments": loss_count,
            "by_type": by_type,
        }

    def get_investment_performance(
        self, investment_id: str, user_id: str
    ) -> Optional[dict]:
        """Get performance metrics for a specific investment."""
        investment = self.get_investment_by_id(investment_id, user_id)
        if not investment:
            return None

        return {
            "investment_id": investment_id,
            "symbol": investment.symbol,
            "name": investment.name,
            "investment_type": investment.investment_type.value,
            "initial_amount": float(investment.initial_amount.amount),
            "current_value": float(investment.current_value.amount),
            "gain_loss_amount": float(investment.gain_loss_amount().amount),
            "gain_loss_percentage": investment.gain_loss_percentage(),
            "is_profitable": investment.is_profitable(),
            "days_held": investment.days_held(),
            "purchase_date": investment.purchase_date.isoformat(),
        }
