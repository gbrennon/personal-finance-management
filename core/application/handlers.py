from core.domain.messages import MessageHandler
from core.domain.events import (
    Event,
    TransactionCreatedEvent,
    BudgetExceededEvent,
    InvoiceCreatedEvent,
    InvestmentCreatedEvent,
    RetirementPlanCreatedEvent,
)
from core.domain.commands import (
    Command,
    CreateTransactionCommand,
    UpdateTransactionCommand,
    DeleteTransactionCommand,
    CreateBudgetCommand,
    CreateInvoiceCommand,
    CreateInvestmentCommand,
    CreateRetirementPlanCommand,
    GenerateForecastCommand,
)
from django.contrib.auth.models import User
from finance.models import (
    Transaction,
    Budget,
    Category,
    Invoice,
    Investment,
    RetirementPlan,
)
from decimal import Decimal
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TransactionCreatedEventHandler(MessageHandler):
    """Handler for TransactionCreatedEvent"""

    def can_handle(self, message) -> bool:
        return isinstance(message, TransactionCreatedEvent)

    async def handle(self, message: TransactionCreatedEvent) -> None:
        logger.info(f"Handling TransactionCreatedEvent: {message.data}")
        # Here you could add additional business logic like:
        # - Send notifications
        # - Update analytics
        # - Trigger other processes
        pass


class BudgetExceededEventHandler(MessageHandler):
    """Handler for BudgetExceededEvent"""

    def can_handle(self, message) -> bool:
        return isinstance(message, BudgetExceededEvent)

    async def handle(self, message: BudgetExceededEvent) -> None:
        logger.info(f"Handling BudgetExceededEvent: {message.data}")
        # Here you could add logic like:
        # - Send email notifications
        # - Create alerts
        # - Log budget violations
        pass


class CreateTransactionCommandHandler(MessageHandler):
    """Handler for CreateTransactionCommand"""

    def can_handle(self, message) -> bool:
        return isinstance(message, CreateTransactionCommand)

    async def handle(self, message: CreateTransactionCommand) -> None:
        logger.info(f"Handling CreateTransactionCommand: {message.data}")

        try:
            data = message.data
            user = User.objects.get(id=data["user_id"])

            # Get or create category
            category, created = Category.objects.get_or_create(
                user=user,
                name=data["category"],
                transaction_type=data["transaction_type"],
            )

            # Create transaction
            transaction = Transaction.objects.create(
                user=user,
                transaction_type=data["transaction_type"],
                amount=Decimal(str(data["amount"])),
                category=category,
                date=datetime.fromisoformat(data["date"]).date(),
            )

            logger.info(f"Transaction created: {transaction.id}")

        except Exception as e:
            logger.error(f"Error creating transaction: {e}")
            raise


class CreateInvoiceCommandHandler(MessageHandler):
    """Handler for CreateInvoiceCommand"""

    def can_handle(self, message) -> bool:
        return isinstance(message, CreateInvoiceCommand)

    async def handle(self, message: CreateInvoiceCommand) -> None:
        logger.info(f"Handling CreateInvoiceCommand: {message.data}")

        try:
            data = message.data
            user = User.objects.get(id=data["user_id"])

            # Generate invoice number
            last_invoice = Invoice.objects.filter(user=user).order_by("-id").first()
            invoice_number = (
                f"INV-{user.id}-{(last_invoice.id + 1) if last_invoice else 1:04d}"
            )

            invoice = Invoice.objects.create(
                user=user,
                invoice_number=invoice_number,
                client_name=data["client_name"],
                amount=Decimal(str(data["amount"])),
                due_date=datetime.fromisoformat(data["due_date"]).date(),
                description=data.get("description", ""),
            )

            logger.info(f"Invoice created: {invoice.id}")

        except Exception as e:
            logger.error(f"Error creating invoice: {e}")
            raise


class CreateInvestmentCommandHandler(MessageHandler):
    """Handler for CreateInvestmentCommand"""

    def can_handle(self, message) -> bool:
        return isinstance(message, CreateInvestmentCommand)

    async def handle(self, message: CreateInvestmentCommand) -> None:
        logger.info(f"Handling CreateInvestmentCommand: {message.data}")

        try:
            data = message.data
            user = User.objects.get(id=data["user_id"])

            investment = Investment.objects.create(
                user=user,
                name=f"{data['investment_type'].title()} Investment",
                investment_type=data["investment_type"],
                amount_invested=Decimal(str(data["amount"])),
                expected_return_rate=Decimal(str(data["expected_return"])),
                risk_level=data.get("risk_level", "medium"),
                purchase_date=datetime.now().date(),
            )

            logger.info(f"Investment created: {investment.id}")

        except Exception as e:
            logger.error(f"Error creating investment: {e}")
            raise


class CreateRetirementPlanCommandHandler(MessageHandler):
    """Handler for CreateRetirementPlanCommand"""

    def can_handle(self, message) -> bool:
        return isinstance(message, CreateRetirementPlanCommand)

    async def handle(self, message: CreateRetirementPlanCommand) -> None:
        logger.info(f"Handling CreateRetirementPlanCommand: {message.data}")

        try:
            data = message.data
            user = User.objects.get(id=data["user_id"])

            # Update or create retirement plan
            retirement_plan, created = RetirementPlan.objects.update_or_create(
                user=user,
                defaults={
                    "target_retirement_amount": Decimal(str(data["target_amount"])),
                    "current_age": data["current_age"],
                    "target_retirement_age": data["target_age"],
                    "monthly_contribution": Decimal(str(data["monthly_contribution"])),
                },
            )

            logger.info(
                f"Retirement plan {'created' if created else 'updated'}: {retirement_plan.id}"
            )

        except Exception as e:
            logger.error(f"Error creating retirement plan: {e}")
            raise


class GenerateForecastCommandHandler(MessageHandler):
    """Handler for GenerateForecastCommand"""

    def can_handle(self, message) -> bool:
        return isinstance(message, GenerateForecastCommand)

    async def handle(self, message: GenerateForecastCommand) -> None:
        logger.info(f"Handling GenerateForecastCommand: {message.data}")

        try:
            data = message.data
            user = User.objects.get(id=data["user_id"])

            # Here you would implement the forecasting logic
            # This is a placeholder for the ML forecasting functionality
            logger.info(f"Generating forecast for user {user.id}")

        except Exception as e:
            logger.error(f"Error generating forecast: {e}")
            raise
