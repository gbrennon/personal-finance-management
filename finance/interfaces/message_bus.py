from abc import ABC, abstractmethod
from typing import Any, Dict


class MessageBus(ABC):
    """Abstract interface for message bus operations"""

    @abstractmethod
    def publish(self, topic: str, message: Dict[str, Any]) -> None:
        """Publish a message to a topic"""
        pass

    @abstractmethod
    def subscribe(self, topic: str, callback) -> None:
        """Subscribe to a topic with a callback function"""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the message bus connection"""
        pass
