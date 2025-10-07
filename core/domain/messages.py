from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime
from uuid import uuid4
import json


class Message(ABC):
    """Base class for all messages in the system"""

    def __init__(
        self, message_id: Optional[str] = None, timestamp: Optional[datetime] = None
    ):
        self.message_id = message_id or str(uuid4())
        self.timestamp = timestamp or datetime.utcnow()
        self.metadata: Dict[str, Any] = {}

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization"""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """Create message from dictionary"""
        pass

    def to_json(self) -> str:
        """Convert message to JSON string"""
        return json.dumps(self.to_dict(), default=str)

    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the message"""
        self.metadata[key] = value


class MessageHandler(ABC):
    """Base class for all message handlers"""

    @abstractmethod
    async def handle(self, message: Message) -> None:
        """Handle the incoming message"""
        pass

    @abstractmethod
    def can_handle(self, message: Message) -> bool:
        """Check if this handler can process the given message"""
        pass


class MessageDispatcher:
    """Dispatches messages to appropriate handlers"""

    def __init__(self):
        self._handlers: Dict[str, MessageHandler] = {}

    def register_handler(self, message_type: str, handler: MessageHandler) -> None:
        """Register a handler for a specific message type"""
        self._handlers[message_type] = handler

    async def dispatch(self, message: Message) -> None:
        """Dispatch message to the appropriate handler"""
        message_type = message.__class__.__name__

        if message_type in self._handlers:
            handler = self._handlers[message_type]
            if handler.can_handle(message):
                await handler.handle(message)
            else:
                raise ValueError(
                    f"Handler for {message_type} cannot process this message"
                )
        else:
            raise ValueError(f"No handler registered for message type: {message_type}")
