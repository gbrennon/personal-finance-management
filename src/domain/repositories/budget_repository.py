from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.budget import Budget
from ..value_objects.budget_id import BudgetId
from ..value_objects.user_id import UserId


class BudgetRepository(ABC):
    """Abstract repository for budget entities."""

    @abstractmethod
    def save(self, budget: Budget) -> None:
        """Save a budget."""
        pass

    @abstractmethod
    def get_by_id(self, budget_id: BudgetId) -> Optional[Budget]:
        """Get a budget by its ID."""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: UserId) -> List[Budget]:
        """Get all budgets for a user."""
        pass

    @abstractmethod
    def get_by_user_and_month_year(
        self, user_id: UserId, month: int, year: int
    ) -> Optional[Budget]:
        """Get a budget for a user in a specific month and year."""
        pass

    @abstractmethod
    def delete(self, budget_id: BudgetId) -> None:
        """Delete a budget."""
        pass

    @abstractmethod
    def exists(self, budget_id: BudgetId) -> bool:
        """Check if a budget exists."""
        pass
