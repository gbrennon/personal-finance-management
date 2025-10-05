"""
Event bus for managing domain events and commands.
"""

import logging
from typing import List, Dict, Any
from foundations.domain.aggregate_root import DomainEvent
from .kafka_producer import KafkaEventProducer

logger = logging.getLogger(__name__)


class EventBus:
    """
    Event bus for publishing and managing domain events.
    """

    def __init__(self, kafka_producer: KafkaEventProducer):
        """
        Initialize event bus.

        Args:
            kafka_producer: Kafka producer instance
        """
        self.kafka_producer = kafka_producer

    def publish_events(self, events: List[DomainEvent]) -> bool:
        """
        Publish a list of domain events.

        Args:
            events: List of domain events to publish

        Returns:
            True if all events published successfully, False otherwise
        """
        success = True

        for event in events:
            try:
                result = self.kafka_producer.publish_event(event)
                if not result:
                    success = False
                    logger.error(f"Failed to publish event: {event.event_type}")
            except Exception as e:
                success = False
                logger.error(f"Error publishing event {event.event_type}: {str(e)}")

        return success

    def publish_command(
        self, command_data: Dict[str, Any], target_service: str
    ) -> bool:
        """
        Publish a command to a target service.

        Args:
            command_data: Command data dictionary
            target_service: Target service name

        Returns:
            True if command published successfully, False otherwise
        """
        topic = f"commands.{target_service.lower()}"

        try:
            return self.kafka_producer.publish_command(command_data, topic)
        except Exception as e:
            logger.error(f"Error publishing command to {target_service}: {str(e)}")
            return False
