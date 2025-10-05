"""
Base Entity class for domain entities.
"""

from abc import ABC
from typing import Any, Dict, Optional
import uuid
from datetime import datetime


class Entity(ABC):
    """
    Base class for all domain entities.

    An entity is an object that has a distinct identity that runs through time
    and different representations. It is defined by its identity, not by its attributes.
    """

    def __init__(self, entity_id: Optional[str] = None):
        """
        Initialize the entity with a unique identifier.

        Args:
            entity_id: Unique identifier for the entity. If None, a new UUID will be generated.
        """
        self._id = entity_id or str(uuid.uuid4())
        self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()

    @property
    def id(self) -> str:
        """Get the entity's unique identifier."""
        return self._id

    @property
    def created_at(self) -> datetime:
        """Get the entity's creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Get the entity's last update timestamp."""
        return self._updated_at

    def _update_timestamp(self) -> None:
        """Update the entity's last update timestamp."""
        self._updated_at = datetime.utcnow()

    def __eq__(self, other: object) -> bool:
        """
        Two entities are equal if they have the same ID and are of the same type.
        """
        if not isinstance(other, Entity):
            return False
        return self._id == other._id and type(self) == type(other)

    def __hash__(self) -> int:
        """Hash based on entity ID and type."""
        return hash((self._id, type(self)))

    def __repr__(self) -> str:
        """String representation of the entity."""
        return f"{self.__class__.__name__}(id={self._id})"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert entity to dictionary representation.
        Subclasses should override this method to include their specific attributes.
        """
        return {
            "id": self._id,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
        }
