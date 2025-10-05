"""
Django management command to run the notifications Kafka consumer.
"""

import logging
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings

from shared.infrastructure.kafka_consumer import KafkaEventConsumer
from notifications.models import Notification

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run the notifications Kafka consumer"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting notifications consumer..."))

        # Initialize Kafka consumer
        consumer = KafkaEventConsumer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id="notifications-service",
        )

        # Subscribe to finance events
        topics = [
            "finance.transactioncreated",
            "finance.budgetexceeded",
            "finance.budgetcreated",
        ]
        consumer.subscribe_to_topics(topics)

        # Register event handlers
        consumer.register_handler("TransactionCreated", self.handle_transaction_created)
        consumer.register_handler("BudgetExceeded", self.handle_budget_exceeded)
        consumer.register_handler("BudgetCreated", self.handle_budget_created)

        try:
            # Start consuming
            consumer.start_consuming()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Consumer stopped by user"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Consumer error: {str(e)}"))
        finally:
            consumer.close()

    def handle_transaction_created(self, event_data):
        """Handle TransactionCreated event."""
        try:
            data = event_data.get("data", {})
            user_id = data.get("user_id")
            transaction_type = data.get("transaction_type")
            amount = data.get("amount")

            if user_id:
                user = User.objects.get(pk=int(user_id))

                notification = Notification.objects.create(
                    user=user,
                    notification_type="transaction_created",
                    title=f"New {transaction_type} Added",
                    message=f"A new {transaction_type.lower()} of ${amount} has been added to your account.",
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created notification for transaction: {notification.pk}"
                    )
                )

        except Exception as e:
            logger.error(f"Error handling TransactionCreated event: {str(e)}")

    def handle_budget_exceeded(self, event_data):
        """Handle BudgetExceeded event."""
        try:
            data = event_data.get("data", {})
            user_id = data.get("user_id")
            budget_amount = data.get("budget_amount")
            actual_amount = data.get("actual_amount")
            month = data.get("month")
            year = data.get("year")

            if user_id:
                user = User.objects.get(pk=int(user_id))

                notification = Notification.objects.create(
                    user=user,
                    notification_type="budget_exceeded",
                    title="Budget Exceeded!",
                    message=f"Your budget of ${budget_amount} for {month}/{year} has been exceeded. "
                    f"Current spending: ${actual_amount}",
                )

                self.stdout.write(
                    self.style.WARNING(
                        f"Created budget exceeded notification: {notification.pk}"
                    )
                )

        except Exception as e:
            logger.error(f"Error handling BudgetExceeded event: {str(e)}")

    def handle_budget_created(self, event_data):
        """Handle BudgetCreated event."""
        try:
            data = event_data.get("data", {})
            user_id = data.get("user_id")
            amount = data.get("amount")
            month = data.get("month")
            year = data.get("year")

            if user_id:
                user = User.objects.get(pk=int(user_id))

                notification = Notification.objects.create(
                    user=user,
                    notification_type="budget_created",
                    title="Budget Set",
                    message=f"Your budget of ${amount} for {month}/{year} has been set successfully.",
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created budget notification: {notification.pk}"
                    )
                )

        except Exception as e:
            logger.error(f"Error handling BudgetCreated event: {str(e)}")
