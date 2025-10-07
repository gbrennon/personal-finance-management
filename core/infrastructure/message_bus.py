from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from core.domain.messages import Message
import asyncio
import json
import logging
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import threading

logger = logging.getLogger(__name__)


class MessageBus(ABC):
    """Abstract interface for message bus implementations"""

    @abstractmethod
    async def publish(self, topic: str, message: Message) -> None:
        """Publish a message to a topic"""
        pass

    @abstractmethod
    async def subscribe(self, topic: str, handler) -> None:
        """Subscribe to a topic with a handler"""
        pass

    @abstractmethod
    async def start(self) -> None:
        """Start the message bus"""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Stop the message bus"""
        pass


class KafkaMessageBus(MessageBus):
    """Kafka implementation of the MessageBus interface"""

    def __init__(self, bootstrap_servers: List[str] = None):
        self.bootstrap_servers = bootstrap_servers or ["kafka:9092"]
        self.producer: Optional[KafkaProducer] = None
        self.consumers: Dict[str, KafkaConsumer] = {}
        self.consumer_threads: Dict[str, threading.Thread] = {}
        self.running = False

    async def start(self) -> None:
        """Start the Kafka message bus"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: k.encode("utf-8") if k else None,
                retries=3,
                acks="all",
            )
            self.running = True
            logger.info("Kafka MessageBus started successfully")
        except Exception as e:
            logger.error(f"Failed to start Kafka MessageBus: {e}")
            raise

    async def stop(self) -> None:
        """Stop the Kafka message bus"""
        self.running = False

        # Stop all consumer threads
        for topic, thread in self.consumer_threads.items():
            if thread.is_alive():
                thread.join(timeout=5)

        # Close all consumers
        for consumer in self.consumers.values():
            consumer.close()

        # Close producer
        if self.producer:
            self.producer.close()

        logger.info("Kafka MessageBus stopped")

    async def publish(self, topic: str, message: Message) -> None:
        """Publish a message to a Kafka topic"""
        if not self.producer:
            raise RuntimeError("MessageBus not started. Call start() first.")

        try:
            message_data = message.to_dict()
            future = self.producer.send(
                topic, value=message_data, key=message.message_id
            )

            # Wait for the message to be sent
            record_metadata = future.get(timeout=10)
            logger.info(
                f"Message {message.message_id} sent to topic {topic} "
                f"at partition {record_metadata.partition} "
                f"offset {record_metadata.offset}"
            )

        except KafkaError as e:
            logger.error(f"Failed to publish message to topic {topic}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error publishing message: {e}")
            raise

    async def subscribe(self, topic: str, handler) -> None:
        """Subscribe to a Kafka topic with a message handler"""
        if topic in self.consumers:
            logger.warning(f"Already subscribed to topic {topic}")
            return

        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                key_deserializer=lambda k: k.decode("utf-8") if k else None,
                group_id=f"finance_app_{topic}",
                auto_offset_reset="earliest",
                enable_auto_commit=True,
            )

            self.consumers[topic] = consumer

            # Start consumer thread
            consumer_thread = threading.Thread(
                target=self._consume_messages,
                args=(topic, consumer, handler),
                daemon=True,
            )
            consumer_thread.start()
            self.consumer_threads[topic] = consumer_thread

            logger.info(f"Subscribed to topic {topic}")

        except Exception as e:
            logger.error(f"Failed to subscribe to topic {topic}: {e}")
            raise

    def _consume_messages(self, topic: str, consumer: KafkaConsumer, handler):
        """Internal method to consume messages in a separate thread"""
        logger.info(f"Started consuming messages from topic {topic}")

        try:
            for message in consumer:
                if not self.running:
                    break

                try:
                    # Process the message
                    message_data = message.value
                    logger.info(f"Received message from topic {topic}: {message_data}")

                    # Call the handler asynchronously
                    asyncio.run(handler(message_data))

                except Exception as e:
                    logger.error(f"Error processing message from topic {topic}: {e}")

        except Exception as e:
            logger.error(f"Error in consumer for topic {topic}: {e}")
        finally:
            logger.info(f"Stopped consuming messages from topic {topic}")


class InMemoryMessageBus(MessageBus):
    """In-memory implementation for testing purposes"""

    def __init__(self):
        self.subscribers: Dict[str, List] = {}
        self.running = False

    async def start(self) -> None:
        self.running = True
        logger.info("InMemory MessageBus started")

    async def stop(self) -> None:
        self.running = False
        logger.info("InMemory MessageBus stopped")

    async def publish(self, topic: str, message: Message) -> None:
        if not self.running:
            raise RuntimeError("MessageBus not started")

        if topic in self.subscribers:
            for handler in self.subscribers[topic]:
                try:
                    await handler(message.to_dict())
                except Exception as e:
                    logger.error(f"Error in handler for topic {topic}: {e}")

    async def subscribe(self, topic: str, handler) -> None:
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)
        logger.info(f"Subscribed to topic {topic}")
