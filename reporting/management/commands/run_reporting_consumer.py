"""
Django management command to run the reporting Kafka consumer.
"""

import logging
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

from shared.infrastructure.kafka_consumer import KafkaEventConsumer
from reporting.models import ReportMetrics

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run the reporting Kafka consumer"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting reporting consumer..."))

        # Initialize Kafka consumer
        consumer = KafkaEventConsumer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id="reporting-service",
        )

        # Subscribe to finance events
        topics = [
            "finance.transactioncreated",
            "finance.budgetcreated",
        ]
        consumer.subscribe_to_topics(topics)

        # Register event handlers
        consumer.register_handler("TransactionCreated", self.handle_transaction_created)
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
        """Handle TransactionCreated event and update metrics."""
        try:
            data = event_data.get("data", {})
            user_id = data.get("user_id")
            transaction_type = data.get("transaction_type")
            amount = Decimal(str(data.get("amount", 0)))
            transaction_date = data.get("transaction_date")

            if user_id and transaction_date:
                user = User.objects.get(pk=int(user_id))

                # Parse date to get month and year
                from datetime import datetime

                date_obj = datetime.fromisoformat(transaction_date)
                month = date_obj.month
                year = date_obj.year

                # Get or create metrics for this user/month/year
                metrics, created = ReportMetrics.objects.get_or_create(
                    user=user,
                    month=month,
                    year=year,
                    defaults={
                        "total_income": Decimal("0.00"),
                        "total_expenses": Decimal("0.00"),
                        "total_savings": Decimal("0.00"),
                        "transaction_count": 0,
                        "income_count": 0,
                        "expense_count": 0,
                    },
                )

                # Update metrics based on transaction type
                if transaction_type == "Income":
                    metrics.total_income += amount
                    metrics.income_count += 1
                elif transaction_type == "Expense":
                    metrics.total_expenses += amount
                    metrics.expense_count += 1

                # Update totals
                metrics.transaction_count += 1
                metrics.total_savings = metrics.total_income - metrics.total_expenses
                metrics.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Updated metrics for {user.username} - {month}/{year}: "
                        f"{transaction_type} ${amount}"
                    )
                )

        except Exception as e:
            logger.error(f"Error handling TransactionCreated event: {str(e)}")

    def handle_budget_created(self, event_data):
        """Handle BudgetCreated event and update metrics."""
        try:
            data = event_data.get("data", {})
            user_id = data.get("user_id")
            amount = data.get("amount")
            month = data.get("month")
            year = data.get("year")

            if user_id and amount:
                user = User.objects.get(pk=int(user_id))
                budget_amount = Decimal(str(amount))

                # Get or create metrics for this user/month/year
                metrics, created = ReportMetrics.objects.get_or_create(
                    user=user,
                    month=month,
                    year=year,
                    defaults={
                        "total_income": Decimal("0.00"),
                        "total_expenses": Decimal("0.00"),
                        "total_savings": Decimal("0.00"),
                        "transaction_count": 0,
                        "income_count": 0,
                        "expense_count": 0,
                    },
                )

                # Update budget information
                metrics.budget_amount = budget_amount

                # Calculate budget utilization if there are expenses
                if metrics.total_expenses > 0 and budget_amount > 0:
                    utilization = (metrics.total_expenses / budget_amount) * 100
                    metrics.budget_utilization = min(
                        utilization, Decimal("999.99")
                    )  # Cap at 999.99%

                metrics.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Updated budget metrics for {user.username} - {month}/{year}: "
                        f"Budget ${budget_amount}"
                    )
                )

        except Exception as e:
            logger.error(f"Error handling BudgetCreated event: {str(e)}")
