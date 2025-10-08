from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.investment import Investment, InvestmentType
from ..value_objects.investment_id import InvestmentId
from ..value_objects.user_id import UserId


class InvestmentRepository(ABC):
    """Abstract repository for investment entities."""

    @abstractmethod
    def save(self, investment: Investment) -> None:
        """Save an investment."""
        pass

    @abstractmethod
    def get_by_id(self, investment_id: InvestmentId) -> Optional[Investment]:
        """Get an investment by its ID."""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: UserId) -> List[Investment]:
        """Get all investments for a user."""
        pass

    @abstractmethod
    def get_by_user_and_type(
        self, user_id: UserId, investment_type: InvestmentType
    ) -> List[Investment]:
        """Get all investments for a user by type."""
        pass

    @abstractmethod
    def get_by_user_and_symbol(self, user_id: UserId, symbol: str) -> List[Investment]:
        """Get all investments for a user by symbol."""
        pass

    @abstractmethod
    def delete(self, investment_id: InvestmentId) -> None:
        """Delete an investment."""
        pass

    @abstractmethod
    def exists(self, investment_id: InvestmentId) -> bool:
        """Check if an investment exists."""
        pass
