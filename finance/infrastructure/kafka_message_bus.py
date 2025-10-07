import json
import logging
from typing import Any, Dict
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
from finance.interfaces.message_bus import MessageBus


logger = logging.getLogger(__name__)


class KafkaMessageBus(MessageBus):
    """Kafka implementation of the MessageBus interface"""

    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.consumers = {}
        self._initialize_producer()

    def _initialize_producer(self):
        """Initialize Kafka producer"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: k.encode("utf-8") if k else None,
            )
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {e}")
            # For development, we'll create a mock producer
            self.producer = MockKafkaProducer()

    def publish(self, topic: str, message: Dict[str, Any]) -> None:
        """Publish a message to a Kafka topic"""
        try:
            if self.producer:
                future = self.producer.send(topic, value=message)
                # Wait for the message to be sent
                future.get(timeout=10)
                logger.info(f"Message published to topic {topic}: {message}")
        except Exception as e:
            logger.error(f"Failed to publish message to topic {topic}: {e}")

    def subscribe(self, topic: str, callback) -> None:
        """Subscribe to a Kafka topic with a callback function"""
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="latest",
                group_id=f"{topic}_group",
            )
            self.consumers[topic] = consumer

            # In a real application, this would run in a separate thread
            for message in consumer:
                callback(message.value)

        except Exception as e:
            logger.error(f"Failed to subscribe to topic {topic}: {e}")

    def close(self) -> None:
        """Close all Kafka connections"""
        if self.producer:
            self.producer.close()

        for consumer in self.consumers.values():
            consumer.close()

        self.consumers.clear()


class MockKafkaProducer:
    """Mock Kafka producer for development when Kafka is not available"""

    def send(self, topic: str, value: Dict[str, Any], key=None):
        logger.info(f"Mock: Publishing to {topic}: {value}")
        return MockFuture()

    def close(self):
        logger.info("Mock: Closing Kafka producer")


class MockFuture:
    """Mock future for development"""

    def get(self, timeout=None):
        return True
