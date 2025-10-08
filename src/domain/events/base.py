from abc import ABC
from datetime import datetime
from typing import Any, Dict
import uuid


class DomainEvent(ABC):
    """Base class for all domain events."""

    def __init__(self, event_data: Dict[str, Any]):
        self.event_id = str(uuid.uuid4())
        self.occurred_at = datetime.utcnow()
        self.event_data = event_data

    @property
    def event_type(self) -> str:
        """Return the event type name."""
        return self.__class__.__name__

    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a dictionary."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "occurred_at": self.occurred_at.isoformat(),
            "event_data": self.event_data,
        }

    def __str__(self) -> str:
        return f"{self.event_type}({self.event_id})"

    def __repr__(self) -> str:
        return f"{self.event_type}(event_id='{self.event_id}', occurred_at='{self.occurred_at}')"
