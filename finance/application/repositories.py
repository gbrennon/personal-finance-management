"""
Repository interfaces for Finance application layer.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal

from foundations import Repository
from ..domain.entities import FinanceTransaction, Budget, Category


class TransactionRepository(Repository[FinanceTransaction, str]):
    """
    Repository interface for FinanceTransaction entities.
    """

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> List[FinanceTransaction]:
        """Find all transactions for a specific user."""
        pass

    @abstractmethod
    def find_by_user_and_type(
        self, user_id: str, transaction_type: str
    ) -> List[FinanceTransaction]:
        """Find transactions by user and type."""
        pass

    @abstractmethod
    def find_by_user_and_date_range(
        self, user_id: str, month: int, year: int
    ) -> List[FinanceTransaction]:
        """Find transactions by user within a specific month/year."""
        pass

    @abstractmethod
    def get_total_by_type_and_period(
        self, user_id: str, transaction_type: str, month: int, year: int
    ) -> Decimal:
        """Get total amount for a specific transaction type in a given period."""
        pass


class BudgetRepository(Repository[Budget, str]):
    """
    Repository interface for Budget entities.
    """

    @abstractmethod
    def find_by_user_and_period(
        self, user_id: str, month: int, year: int
    ) -> Optional[Budget]:
        """Find budget for a specific user and period."""
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> List[Budget]:
        """Find all budgets for a specific user."""
        pass


class CategoryRepository(Repository[Category, str]):
    """
    Repository interface for Category entities.
    """

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> List[Category]:
        """Find all categories for a specific user."""
        pass

    @abstractmethod
    def find_by_user_and_type(
        self, user_id: str, transaction_type: str
    ) -> List[Category]:
        """Find categories by user and transaction type."""
        pass

    @abstractmethod
    def find_by_name_and_user(self, name: str, user_id: str) -> Optional[Category]:
        """Find category by name and user."""
        pass
