from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.category import Category, CategoryType
from ..value_objects.category_id import CategoryId
from ..value_objects.user_id import UserId


class CategoryRepository(ABC):
    """Abstract repository for category entities."""

    @abstractmethod
    def save(self, category: Category) -> None:
        """Save a category."""
        pass

    @abstractmethod
    def get_by_id(self, category_id: CategoryId) -> Optional[Category]:
        """Get a category by its ID."""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: UserId) -> List[Category]:
        """Get all categories for a user."""
        pass

    @abstractmethod
    def get_by_user_and_type(
        self, user_id: UserId, category_type: CategoryType
    ) -> List[Category]:
        """Get all categories for a user by type."""
        pass

    @abstractmethod
    def get_by_user_and_name(
        self, user_id: UserId, name: str, category_type: CategoryType
    ) -> Optional[Category]:
        """Get a category by user, name, and type."""
        pass

    @abstractmethod
    def delete(self, category_id: CategoryId) -> None:
        """Delete a category."""
        pass

    @abstractmethod
    def exists(self, category_id: CategoryId) -> bool:
        """Check if a category exists."""
        pass
