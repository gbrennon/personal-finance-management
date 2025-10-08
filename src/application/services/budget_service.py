from typing import List, Optional
import uuid

from ...domain.entities.budget import Budget
from ...domain.value_objects.money import Money
from ...domain.value_objects.budget_id import BudgetId
from ...domain.value_objects.user_id import UserId
from ...domain.events.budget_events import (
    BudgetCreated,
    BudgetUpdated,
    BudgetExceeded,
)
from ...domain.repositories.unit_of_work import UnitOfWork
from ..commands.budget_commands import (
    CreateBudgetCommand,
    UpdateBudgetCommand,
)


class BudgetService:
    """Application service for budget operations."""

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def create_budget(self, command: CreateBudgetCommand) -> str:
        """Create a new budget."""
        with self._uow:
            # Check if budget already exists for this month/year
            existing_budget = self._uow.budgets.get_by_user_and_month_year(
                UserId(command.user_id), command.month, command.year
            )
            if existing_budget:
                raise ValueError("Budget already exists for this month and year")

            budget_id = BudgetId(str(uuid.uuid4()))
            amount = Money(command.amount) if command.amount is not None else None

            budget = Budget(
                budget_id=budget_id,
                user_id=UserId(command.user_id),
                month=command.month,
                year=command.year,
                amount=amount,
            )

            self._uow.budgets.save(budget)

            # Add domain event
            event = BudgetCreated(
                budget_id=budget_id.value,
                user_id=command.user_id,
                month=command.month,
                year=command.year,
                amount=str(command.amount) if command.amount is not None else None,
            )
            self._uow.add_event(event)

            return budget_id.value

    def update_budget(self, command: UpdateBudgetCommand) -> None:
        """Update an existing budget."""
        with self._uow:
            budget = self._uow.budgets.get_by_id(BudgetId(command.budget_id))
            if not budget:
                raise ValueError("Budget not found")
            if budget.user_id.value != command.user_id:
                raise ValueError("Budget does not belong to user")

            updated_fields = {}

            if command.amount is not None:
                budget.set_amount(Money(command.amount))
                updated_fields["amount"] = str(command.amount)
            else:
                budget.clear_amount()
                updated_fields["amount"] = None

            self._uow.budgets.save(budget)

            # Add domain event
            event = BudgetUpdated(
                budget_id=command.budget_id,
                user_id=command.user_id,
                updated_fields=updated_fields,
            )
            self._uow.add_event(event)

    def get_user_budgets(self, user_id: str) -> List[Budget]:
        """Get all budgets for a user."""
        return self._uow.budgets.get_by_user_id(UserId(user_id))

    def get_budget_by_month_year(
        self, user_id: str, month: int, year: int
    ) -> Optional[Budget]:
        """Get a budget for a specific month and year."""
        return self._uow.budgets.get_by_user_and_month_year(
            UserId(user_id), month, year
        )

    def check_budget_exceeded(
        self, user_id: str, month: int, year: int, spent_amount: Money
    ) -> bool:
        """Check if a budget is exceeded and raise event if so."""
        budget = self.get_budget_by_month_year(user_id, month, year)
        if not budget or not budget.has_amount_set():
            return False

        if budget.is_exceeded_by(spent_amount):
            # Add domain event for budget exceeded
            if budget.amount is not None:
                excess_amount = spent_amount.subtract(budget.amount)
                event = BudgetExceeded(
                    budget_id=budget.budget_id.value,
                    user_id=user_id,
                    month=month,
                    year=year,
                    budget_amount=str(budget.amount.amount),
                    spent_amount=str(spent_amount.amount),
                    excess_amount=str(excess_amount.amount),
                )
                self._uow.add_event(event)
            return True

        return False

    def get_budget_status(self, user_id: str, month: int, year: int) -> Optional[dict]:
        """Get budget status including spending and remaining amount."""
        budget = self.get_budget_by_month_year(user_id, month, year)
        if not budget:
            return None

        # Get total expenses for the month
        transactions = self._uow.transactions.get_by_user_and_month_year(
            UserId(user_id), month, year
        )

        total_expenses = Money(0)
        for transaction in transactions:
            if transaction.is_expense():
                total_expenses = total_expenses.add(transaction.amount)

        if not budget.has_amount_set():
            return {
                "budget_id": budget.budget_id.value,
                "month": month,
                "year": year,
                "budget_amount": None,
                "spent_amount": float(total_expenses.amount),
                "remaining_amount": None,
                "is_exceeded": False,
                "progress_percentage": 0.0,
            }

        remaining = budget.remaining_amount(total_expenses)
        is_exceeded = budget.is_exceeded_by(total_expenses)
        progress_percentage = (
            min(float(total_expenses.amount / budget.amount.amount * 100), 100.0)
            if budget.amount and budget.amount.amount > 0
            else 0.0
        )

        return {
            "budget_id": budget.budget_id.value,
            "month": month,
            "year": year,
            "budget_amount": float(budget.amount.amount) if budget.amount else None,
            "spent_amount": float(total_expenses.amount),
            "remaining_amount": float(remaining.amount) if remaining else 0.0,
            "is_exceeded": is_exceeded,
            "progress_percentage": progress_percentage,
        }
