from typing import Optional

from ..value_objects.money import Money
from ..value_objects.budget_id import BudgetId
from ..value_objects.user_id import UserId


class Budget:
    """Domain entity representing a monthly budget."""

    def __init__(
        self,
        budget_id: BudgetId,
        user_id: UserId,
        month: int,
        year: int,
        amount: Optional[Money] = None,
    ):
        if not (1 <= month <= 12):
            raise ValueError("Month must be between 1 and 12")
        if year < 1900:
            raise ValueError("Year must be 1900 or later")

        self._budget_id = budget_id
        self._user_id = user_id
        self._month = month
        self._year = year
        self._amount = amount

    @property
    def budget_id(self) -> BudgetId:
        return self._budget_id

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def month(self) -> int:
        return self._month

    @property
    def year(self) -> int:
        return self._year

    @property
    def amount(self) -> Optional[Money]:
        return self._amount

    def set_amount(self, amount: Money) -> None:
        """Set the budget amount."""
        if amount.amount <= 0:
            raise ValueError("Budget amount must be positive")
        self._amount = amount

    def clear_amount(self) -> None:
        """Clear the budget amount (set to None)."""
        self._amount = None

    def has_amount_set(self) -> bool:
        """Check if budget has an amount set."""
        return self._amount is not None

    def is_exceeded_by(self, spent_amount: Money) -> bool:
        """Check if the budget is exceeded by the given spent amount."""
        if not self.has_amount_set() or self._amount is None:
            return False
        return spent_amount.is_greater_than(self._amount)

    def remaining_amount(self, spent_amount: Money) -> Optional[Money]:
        """Calculate remaining budget amount after spending."""
        if not self.has_amount_set() or self._amount is None:
            return None
        try:
            return self._amount.subtract(spent_amount)
        except ValueError:
            # If subtraction would result in negative, budget is exceeded
            return Money(0)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Budget):
            return False
        return self._budget_id == other._budget_id

    def __hash__(self) -> int:
        return hash(self._budget_id)

    def __str__(self) -> str:
        amount_str = str(self._amount) if self._amount else "Not Set"
        return f"Budget({self._budget_id}, {self._month}/{self._year}, {amount_str})"
