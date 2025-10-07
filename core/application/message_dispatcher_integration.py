from core.domain.messages import MessageDispatcher
from core.infrastructure.message_bus import MessageBus
from core.domain.events import Event
from core.domain.commands import Command
import logging

logger = logging.getLogger(__name__)


class MessageDispatcherWithBus(MessageDispatcher):
    """MessageDispatcher that integrates with MessageBus"""

    def __init__(self, message_bus: MessageBus):
        super().__init__()
        self.message_bus = message_bus

    async def dispatch(self, message) -> None:
        """Dispatch message through the message bus"""
        try:
            # Determine topic based on message type
            if isinstance(message, Event):
                topic = f"events.{message.event_type}"
            elif isinstance(message, Command):
                topic = f"commands.{message.command_type}"
            else:
                topic = f"messages.{message.__class__.__name__.lower()}"

            # Publish to message bus
            await self.message_bus.publish(topic, message)

            # Also handle locally if handler is registered
            await super().dispatch(message)

        except Exception as e:
            logger.error(f"Error dispatching message: {e}")
            raise


class MessageBusIntegration:
    """Integration layer for message bus with Django"""

    def __init__(self, message_bus: MessageBus):
        self.message_bus = message_bus
        self.dispatcher = MessageDispatcherWithBus(message_bus)
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup message handlers"""
        from core.application.handlers import (
            TransactionCreatedEventHandler,
            BudgetExceededEventHandler,
            CreateTransactionCommandHandler,
            CreateInvoiceCommandHandler,
            CreateInvestmentCommandHandler,
            CreateRetirementPlanCommandHandler,
            GenerateForecastCommandHandler,
        )

        # Register event handlers
        self.dispatcher.register_handler(
            "TransactionCreatedEvent", TransactionCreatedEventHandler()
        )
        self.dispatcher.register_handler(
            "BudgetExceededEvent", BudgetExceededEventHandler()
        )

        # Register command handlers
        self.dispatcher.register_handler(
            "CreateTransactionCommand", CreateTransactionCommandHandler()
        )
        self.dispatcher.register_handler(
            "CreateInvoiceCommand", CreateInvoiceCommandHandler()
        )
        self.dispatcher.register_handler(
            "CreateInvestmentCommand", CreateInvestmentCommandHandler()
        )
        self.dispatcher.register_handler(
            "CreateRetirementPlanCommand", CreateRetirementPlanCommandHandler()
        )
        self.dispatcher.register_handler(
            "GenerateForecastCommand", GenerateForecastCommandHandler()
        )

    async def start(self):
        """Start the message bus integration"""
        await self.message_bus.start()

        # Subscribe to topics
        await self.message_bus.subscribe(
            "events.transaction_created", self._handle_event_message
        )
        await self.message_bus.subscribe(
            "events.budget_exceeded", self._handle_event_message
        )
        await self.message_bus.subscribe(
            "commands.create_transaction", self._handle_command_message
        )
        await self.message_bus.subscribe(
            "commands.create_invoice", self._handle_command_message
        )
        await self.message_bus.subscribe(
            "commands.create_investment", self._handle_command_message
        )
        await self.message_bus.subscribe(
            "commands.create_retirement_plan", self._handle_command_message
        )
        await self.message_bus.subscribe(
            "commands.generate_forecast", self._handle_command_message
        )

        logger.info("MessageBus integration started")

    async def stop(self):
        """Stop the message bus integration"""
        await self.message_bus.stop()
        logger.info("MessageBus integration stopped")

    async def _handle_event_message(self, message_data):
        """Handle incoming event messages"""
        try:
            from core.domain.events import Event

            # Reconstruct event from message data
            event = Event.from_dict(message_data)
            await self.dispatcher.dispatch(event)
        except Exception as e:
            logger.error(f"Error handling event message: {e}")

    async def _handle_command_message(self, message_data):
        """Handle incoming command messages"""
        try:
            from core.domain.commands import Command

            # Reconstruct command from message data
            command = Command.from_dict(message_data)
            await self.dispatcher.dispatch(command)
        except Exception as e:
            logger.error(f"Error handling command message: {e}")

    def get_dispatcher(self):
        """Get the message dispatcher"""
        return self.dispatcher
