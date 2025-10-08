from abc import ABC, abstractmethod
from typing import List

from ..events.base import DomainEvent
from .transaction_repository import TransactionRepository
from .category_repository import CategoryRepository
from .budget_repository import BudgetRepository
from .retirement_goal_repository import RetirementGoalRepository
from .investment_repository import InvestmentRepository


class UnitOfWork(ABC):
    """Abstract Unit of Work pattern implementation."""

    def __init__(self):
        self._events: List[DomainEvent] = []

    @property
    @abstractmethod
    def transactions(self) -> TransactionRepository:
        """Get the transaction repository."""
        pass

    @property
    @abstractmethod
    def categories(self) -> CategoryRepository:
        """Get the category repository."""
        pass

    @property
    @abstractmethod
    def budgets(self) -> BudgetRepository:
        """Get the budget repository."""
        pass

    @property
    @abstractmethod
    def retirement_goals(self) -> RetirementGoalRepository:
        """Get the retirement goal repository."""
        pass

    @property
    @abstractmethod
    def investments(self) -> InvestmentRepository:
        """Get the investment repository."""
        pass

    @abstractmethod
    def commit(self) -> None:
        """Commit the current transaction."""
        pass

    @abstractmethod
    def rollback(self) -> None:
        """Rollback the current transaction."""
        pass

    def add_event(self, event: DomainEvent) -> None:
        """Add a domain event to be published."""
        self._events.append(event)

    def get_events(self) -> List[DomainEvent]:
        """Get all collected domain events."""
        return self._events.copy()

    def clear_events(self) -> None:
        """Clear all collected domain events."""
        self._events.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
