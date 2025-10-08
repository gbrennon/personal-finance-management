from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date

from ..entities.transaction import Transaction
from ..value_objects.transaction_id import TransactionId
from ..value_objects.user_id import UserId
from ..value_objects.category_id import CategoryId


class TransactionRepository(ABC):
    """Abstract repository for transaction entities."""

    @abstractmethod
    def save(self, transaction: Transaction) -> None:
        """Save a transaction."""
        pass

    @abstractmethod
    def get_by_id(self, transaction_id: TransactionId) -> Optional[Transaction]:
        """Get a transaction by its ID."""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: UserId) -> List[Transaction]:
        """Get all transactions for a user."""
        pass

    @abstractmethod
    def get_by_user_and_category(
        self, user_id: UserId, category_id: CategoryId
    ) -> List[Transaction]:
        """Get all transactions for a user and category."""
        pass

    @abstractmethod
    def get_by_user_and_date_range(
        self, user_id: UserId, start_date: date, end_date: date
    ) -> List[Transaction]:
        """Get all transactions for a user within a date range."""
        pass

    @abstractmethod
    def get_by_user_and_month_year(
        self, user_id: UserId, month: int, year: int
    ) -> List[Transaction]:
        """Get all transactions for a user in a specific month and year."""
        pass

    @abstractmethod
    def delete(self, transaction_id: TransactionId) -> None:
        """Delete a transaction."""
        pass

    @abstractmethod
    def exists(self, transaction_id: TransactionId) -> bool:
        """Check if a transaction exists."""
        pass
