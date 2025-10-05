"""
Base Repository interface for Clean Architecture.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

# Type variable for the entity type
TEntity = TypeVar("TEntity")
TId = TypeVar("TId")


class Repository(ABC, Generic[TEntity, TId]):
    """
    Base interface for repositories in Clean Architecture.

    A repository encapsulates the logic needed to access data sources.
    It centralizes common data access functionality, providing better
    maintainability and decoupling the infrastructure or technology used
    to access databases from the domain model layer.

    Type Parameters:
        TEntity: The type of entity this repository manages
        TId: The type of the entity's identifier
    """

    @abstractmethod
    def save(self, entity: TEntity) -> TEntity:
        """
        Save an entity to the repository.

        Args:
            entity: The entity to save

        Returns:
            The saved entity (may include generated IDs or updated timestamps)
        """
        pass

    @abstractmethod
    def find_by_id(self, entity_id: TId) -> Optional[TEntity]:
        """
        Find an entity by its identifier.

        Args:
            entity_id: The unique identifier of the entity

        Returns:
            The entity if found, None otherwise
        """
        pass

    @abstractmethod
    def find_all(self) -> List[TEntity]:
        """
        Find all entities in the repository.

        Returns:
            List of all entities
        """
        pass

    @abstractmethod
    def delete(self, entity: TEntity) -> None:
        """
        Delete an entity from the repository.

        Args:
            entity: The entity to delete
        """
        pass

    @abstractmethod
    def delete_by_id(self, entity_id: TId) -> bool:
        """
        Delete an entity by its identifier.

        Args:
            entity_id: The unique identifier of the entity to delete

        Returns:
            True if the entity was deleted, False if it wasn't found
        """
        pass

    @abstractmethod
    def exists(self, entity_id: TId) -> bool:
        """
        Check if an entity exists in the repository.

        Args:
            entity_id: The unique identifier of the entity

        Returns:
            True if the entity exists, False otherwise
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """
        Count the total number of entities in the repository.

        Returns:
            The total count of entities
        """
        pass
