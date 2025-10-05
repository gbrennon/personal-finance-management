"""
Kafka event producer for publishing domain events.
"""

import json
import logging
from typing import Dict, Any, Optional
from kafka import KafkaProducer
from kafka.errors import KafkaError

from foundations.domain.aggregate_root import DomainEvent

logger = logging.getLogger(__name__)


class KafkaEventProducer:
    """
    Kafka producer for publishing domain events.
    """

    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        """
        Initialize Kafka producer.

        Args:
            bootstrap_servers: Kafka bootstrap servers
        """
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self._connect()

    def _connect(self) -> None:
        """Connect to Kafka."""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: k.encode("utf-8") if k else None,
                acks="all",
                retries=3,
                retry_backoff_ms=1000,
            )
            logger.info(f"Connected to Kafka at {self.bootstrap_servers}")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {str(e)}")
            raise

    def publish_event(self, event: DomainEvent, topic: Optional[str] = None) -> bool:
        """
        Publish a domain event to Kafka.

        Args:
            event: The domain event to publish
            topic: Kafka topic (defaults to event type)

        Returns:
            True if published successfully, False otherwise
        """
        if not self.producer:
            logger.error("Kafka producer not initialized")
            return False

        try:
            # Use event type as topic if not specified
            if not topic:
                topic = f"finance.{event.event_type.lower()}"

            # Convert event to dictionary
            event_data = event.to_dict()

            # Add metadata
            message = {
                "event_id": event_data.get("aggregate_id"),
                "event_type": event.event_type,
                "aggregate_id": event.aggregate_id,
                "occurred_at": event_data.get("occurred_at"),
                "data": event_data.get("data", {}),
            }

            # Publish to Kafka
            future = self.producer.send(
                topic=topic, key=event.aggregate_id, value=message
            )

            # Wait for confirmation
            record_metadata = future.get(timeout=10)

            logger.info(
                f"Published event {event.event_type} to topic {topic} "
                f"(partition: {record_metadata.partition}, offset: {record_metadata.offset})"
            )

            return True

        except KafkaError as e:
            logger.error(f"Kafka error publishing event: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error publishing event: {str(e)}")
            return False

    def publish_command(self, command_data: Dict[str, Any], topic: str) -> bool:
        """
        Publish a command to Kafka.

        Args:
            command_data: Command data dictionary
            topic: Kafka topic

        Returns:
            True if published successfully, False otherwise
        """
        if not self.producer:
            logger.error("Kafka producer not initialized")
            return False

        try:
            # Publish to Kafka
            future = self.producer.send(
                topic=topic, key=command_data.get("command_id"), value=command_data
            )

            # Wait for confirmation
            record_metadata = future.get(timeout=10)

            logger.info(
                f"Published command to topic {topic} "
                f"(partition: {record_metadata.partition}, offset: {record_metadata.offset})"
            )

            return True

        except KafkaError as e:
            logger.error(f"Kafka error publishing command: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error publishing command: {str(e)}")
            return False

    def close(self) -> None:
        """Close the Kafka producer."""
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer closed")
