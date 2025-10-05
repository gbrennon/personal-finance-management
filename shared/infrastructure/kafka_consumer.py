"""
Kafka event consumer for consuming domain events and commands.
"""

import json
import logging
from typing import Dict, Any, Callable, List
from kafka import KafkaConsumer
from kafka.errors import KafkaError

logger = logging.getLogger(__name__)


class KafkaEventConsumer:
    """
    Kafka consumer for consuming domain events and commands.
    """

    def __init__(
        self, bootstrap_servers: str = "localhost:9092", group_id: str = "finance-app"
    ):
        """
        Initialize Kafka consumer.

        Args:
            bootstrap_servers: Kafka bootstrap servers
            group_id: Consumer group ID
        """
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer = None
        self.handlers: Dict[str, List[Callable]] = {}
        self._connect()

    def _connect(self) -> None:
        """Connect to Kafka."""
        try:
            self.consumer = KafkaConsumer(
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                key_deserializer=lambda k: k.decode("utf-8") if k else None,
                auto_offset_reset="latest",
                enable_auto_commit=True,
                auto_commit_interval_ms=1000,
            )
            logger.info(f"Connected to Kafka consumer at {self.bootstrap_servers}")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka consumer: {str(e)}")
            raise

    def subscribe_to_topics(self, topics: List[str]) -> None:
        """
        Subscribe to Kafka topics.

        Args:
            topics: List of topics to subscribe to
        """
        if not self.consumer:
            logger.error("Kafka consumer not initialized")
            return

        try:
            self.consumer.subscribe(topics)
            logger.info(f"Subscribed to topics: {topics}")
        except Exception as e:
            logger.error(f"Error subscribing to topics: {str(e)}")

    def register_handler(
        self, event_type: str, handler: Callable[[Dict[str, Any]], None]
    ) -> None:
        """
        Register an event handler for a specific event type.

        Args:
            event_type: The event type to handle
            handler: The handler function
        """
        if event_type not in self.handlers:
            self.handlers[event_type] = []

        self.handlers[event_type].append(handler)
        logger.info(f"Registered handler for event type: {event_type}")

    def start_consuming(self) -> None:
        """
        Start consuming messages from Kafka.
        """
        if not self.consumer:
            logger.error("Kafka consumer not initialized")
            return

        logger.info("Starting Kafka consumer...")

        try:
            for message in self.consumer:
                try:
                    # Parse message
                    event_data = message.value
                    event_type = event_data.get("event_type")

                    logger.info(
                        f"Received event: {event_type} from topic: {message.topic}"
                    )

                    # Handle the event
                    if event_type and event_type in self.handlers:
                        for handler in self.handlers[event_type]:
                            try:
                                handler(event_data)
                            except Exception as e:
                                logger.error(
                                    f"Error in event handler for {event_type}: {str(e)}"
                                )
                    else:
                        logger.warning(
                            f"No handler registered for event type: {event_type}"
                        )

                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")

        except KeyboardInterrupt:
            logger.info("Consumer interrupted by user")
        except Exception as e:
            logger.error(f"Error in consumer loop: {str(e)}")
        finally:
            self.close()

    def close(self) -> None:
        """Close the Kafka consumer."""
        if self.consumer:
            self.consumer.close()
            logger.info("Kafka consumer closed")
