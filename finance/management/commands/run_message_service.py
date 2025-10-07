import asyncio
import signal
import sys
from django.core.management.base import BaseCommand
from django.conf import settings
from core.infrastructure.message_bus import KafkaMessageBus, InMemoryMessageBus
from core.application.message_dispatcher_integration import MessageBusIntegration
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run the message service for handling distributed messages"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_bus_integration = None
        self.running = False

    def add_arguments(self, parser):
        parser.add_argument(
            "--bus-type",
            type=str,
            default=getattr(settings, "MESSAGE_BUS_TYPE", "kafka"),
            help="Message bus type: kafka or inmemory",
        )

    def handle(self, *args, **options):
        """Main entry point for the command"""
        bus_type = options["bus_type"]

        self.stdout.write(
            self.style.SUCCESS(
                f"Starting message service with {bus_type} message bus..."
            )
        )

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        try:
            # Run the async main function
            asyncio.run(self._run_service(bus_type))
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Received interrupt signal"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error running message service: {e}"))
            logger.error(f"Error running message service: {e}", exc_info=True)
        finally:
            self.stdout.write(self.style.SUCCESS("Message service stopped"))

    async def _run_service(self, bus_type):
        """Run the message service"""
        try:
            # Create message bus based on type
            if bus_type.lower() == "kafka":
                message_bus = KafkaMessageBus(
                    bootstrap_servers=getattr(
                        settings, "KAFKA_BOOTSTRAP_SERVERS", ["localhost:9092"]
                    )
                )
            else:
                message_bus = InMemoryMessageBus()

            # Create integration
            self.message_bus_integration = MessageBusIntegration(message_bus)

            # Start the service
            await self.message_bus_integration.start()
            self.running = True

            self.stdout.write(
                self.style.SUCCESS("Message service started successfully")
            )

            # Keep the service running
            while self.running:
                await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"Error in message service: {e}", exc_info=True)
            raise
        finally:
            if self.message_bus_integration:
                await self.message_bus_integration.stop()

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.stdout.write(
            self.style.WARNING(f"Received signal {signum}, shutting down...")
        )
        self.running = False
