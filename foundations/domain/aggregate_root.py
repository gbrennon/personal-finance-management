"""
Base AggregateRoot class for domain aggregates.
"""

from typing import List, Any, Dict, Optional
from .entity import Entity


class DomainEvent:
    """
    Base class for domain events.
    """

    def __init__(
        self, aggregate_id: str, event_type: str, data: Optional[Dict[str, Any]] = None
    ):
        self.aggregate_id = aggregate_id
        self.event_type = event_type
        self.data = data or {}
        from datetime import datetime

        self.occurred_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "aggregate_id": self.aggregate_id,
            "event_type": self.event_type,
            "data": self.data,
            "occurred_at": self.occurred_at.isoformat(),
        }


class AggregateRoot(Entity):
    """
    Base class for aggregate roots in Domain-Driven Design.

    An aggregate root is the only member of its aggregate that outside objects
    are allowed to hold references to. It controls access to the aggregate
    and maintains its invariants.
    """

    def __init__(self, entity_id: Optional[str] = None):
        super().__init__(entity_id)
        self._domain_events: List[DomainEvent] = []
        self._version = 0

    @property
    def version(self) -> int:
        """Get the aggregate's version number."""
        return self._version

    def _increment_version(self) -> None:
        """Increment the aggregate's version number."""
        self._version += 1
        self._update_timestamp()

    def _add_domain_event(self, event: DomainEvent) -> None:
        """
        Add a domain event to the aggregate.

        Args:
            event: The domain event to add
        """
        self._domain_events.append(event)
        self._increment_version()

    def get_uncommitted_events(self) -> List[DomainEvent]:
        """
        Get all uncommitted domain events.

        Returns:
            List of uncommitted domain events
        """
        return self._domain_events.copy()

    def mark_events_as_committed(self) -> None:
        """
        Mark all domain events as committed by clearing the events list.
        This should be called after events have been successfully persisted.
        """
        self._domain_events.clear()

    def load_from_history(self, events: List[DomainEvent]) -> None:
        """
        Load the aggregate from a list of historical events.

        Args:
            events: List of historical domain events
        """
        for event in events:
            self._apply_event(event)
            self._version += 1
        self._domain_events.clear()  # Historical events are already committed

    def _apply_event(self, event: DomainEvent) -> None:
        """
        Apply a domain event to the aggregate.
        Subclasses should override this method to handle specific events.

        Args:
            event: The domain event to apply
        """
        pass

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert aggregate root to dictionary representation.
        """
        base_dict = super().to_dict()
        base_dict.update(
            {
                "version": self._version,
                "uncommitted_events_count": len(self._domain_events),
            }
        )
        return base_dict
