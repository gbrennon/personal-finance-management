from datetime import date
from typing import Optional

from ..value_objects.money import Money
from ..value_objects.retirement_goal_id import RetirementGoalId
from ..value_objects.user_id import UserId


class RetirementGoal:
    """Domain entity representing a retirement savings goal."""

    def __init__(
        self,
        goal_id: RetirementGoalId,
        user_id: UserId,
        target_amount: Money,
        target_date: date,
        current_amount: Optional[Money] = None,
        description: Optional[str] = None,
    ):
        if target_date <= date.today():
            raise ValueError("Target date must be in the future")

        self._goal_id = goal_id
        self._user_id = user_id
        self._target_amount = target_amount
        self._target_date = target_date
        self._current_amount = current_amount or Money(0)
        self._description = description

    @property
    def goal_id(self) -> RetirementGoalId:
        return self._goal_id

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def target_amount(self) -> Money:
        return self._target_amount

    @property
    def target_date(self) -> date:
        return self._target_date

    @property
    def current_amount(self) -> Money:
        return self._current_amount

    @property
    def description(self) -> Optional[str]:
        return self._description

    def add_contribution(self, amount: Money) -> None:
        """Add a contribution to the retirement goal."""
        if amount.amount <= 0:
            raise ValueError("Contribution amount must be positive")
        self._current_amount = self._current_amount.add(amount)

    def update_target_amount(self, new_target: Money) -> None:
        """Update the target amount."""
        if new_target.amount <= 0:
            raise ValueError("Target amount must be positive")
        self._target_amount = new_target

    def update_target_date(self, new_date: date) -> None:
        """Update the target date."""
        if new_date <= date.today():
            raise ValueError("Target date must be in the future")
        self._target_date = new_date

    def update_description(self, description: Optional[str]) -> None:
        """Update the description."""
        self._description = description

    def progress_percentage(self) -> float:
        """Calculate the progress percentage towards the goal."""
        if self._target_amount.amount == 0:
            return 0.0
        return min(
            float(self._current_amount.amount / self._target_amount.amount * 100), 100.0
        )

    def remaining_amount(self) -> Money:
        """Calculate the remaining amount needed to reach the goal."""
        try:
            return self._target_amount.subtract(self._current_amount)
        except ValueError:
            # Goal already reached or exceeded
            return Money(0)

    def is_goal_reached(self) -> bool:
        """Check if the retirement goal has been reached."""
        return self._current_amount.is_greater_than(
            self._target_amount
        ) or self._current_amount.is_equal_to(self._target_amount)

    def days_until_target(self) -> int:
        """Calculate days until target date."""
        return (self._target_date - date.today()).days

    def monthly_savings_needed(self) -> Money:
        """Calculate monthly savings needed to reach the goal."""
        from decimal import Decimal

        remaining = self.remaining_amount()
        days_left = self.days_until_target()

        if days_left <= 0 or remaining.amount == 0:
            return Money(0)

        months_left = max(1, days_left / 30.44)  # Average days per month
        monthly_needed = remaining.amount / Decimal(str(months_left))
        return Money(monthly_needed)

    def __eq__(self, other) -> bool:
        if not isinstance(other, RetirementGoal):
            return False
        return self._goal_id == other._goal_id

    def __hash__(self) -> int:
        return hash(self._goal_id)

    def __str__(self) -> str:
        return f"RetirementGoal({self._goal_id}, Target: {self._target_amount}, Current: {self._current_amount})"
