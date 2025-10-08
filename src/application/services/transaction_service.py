from typing import List, Optional
import uuid

from ...domain.entities.transaction import Transaction, TransactionType
from ...domain.value_objects.money import Money
from ...domain.value_objects.transaction_id import TransactionId
from ...domain.value_objects.user_id import UserId
from ...domain.value_objects.category_id import CategoryId
from ...domain.events.transaction_events import (
    TransactionCreated,
    TransactionUpdated,
    TransactionDeleted,
)
from ...domain.repositories.unit_of_work import UnitOfWork
from ..commands.transaction_commands import (
    CreateTransactionCommand,
    UpdateTransactionCommand,
    DeleteTransactionCommand,
)


class TransactionService:
    """Application service for transaction operations."""

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def create_transaction(self, command: CreateTransactionCommand) -> str:
        """Create a new transaction."""
        with self._uow:
            # Validate category exists and belongs to user
            category = self._uow.categories.get_by_id(CategoryId(command.category_id))
            if not category:
                raise ValueError("Category not found")
            if category.user_id.value != command.user_id:
                raise ValueError("Category does not belong to user")

            # Create transaction
            transaction_id = TransactionId(str(uuid.uuid4()))
            transaction_type = (
                TransactionType.INCOME
                if command.transaction_type == "Income"
                else TransactionType.EXPENSE
            )

            transaction = Transaction(
                transaction_id=transaction_id,
                user_id=UserId(command.user_id),
                transaction_type=transaction_type,
                amount=Money(command.amount),
                category_id=CategoryId(command.category_id),
                transaction_date=command.transaction_date,
                description=command.description,
            )

            self._uow.transactions.save(transaction)

            # Add domain event
            event = TransactionCreated(
                transaction_id=transaction_id.value,
                user_id=command.user_id,
                transaction_type=command.transaction_type,
                amount=str(command.amount),
                category_id=command.category_id,
                transaction_date=command.transaction_date.isoformat(),
            )
            self._uow.add_event(event)

            return transaction_id.value

    def update_transaction(self, command: UpdateTransactionCommand) -> None:
        """Update an existing transaction."""
        with self._uow:
            transaction = self._uow.transactions.get_by_id(
                TransactionId(command.transaction_id)
            )
            if not transaction:
                raise ValueError("Transaction not found")
            if transaction.user_id.value != command.user_id:
                raise ValueError("Transaction does not belong to user")

            updated_fields = {}

            if command.amount is not None:
                transaction.update_amount(Money(command.amount))
                updated_fields["amount"] = str(command.amount)

            if command.category_id is not None:
                # Validate category exists and belongs to user
                category = self._uow.categories.get_by_id(
                    CategoryId(command.category_id)
                )
                if not category:
                    raise ValueError("Category not found")
                if category.user_id.value != command.user_id:
                    raise ValueError("Category does not belong to user")

                transaction.update_category(CategoryId(command.category_id))
                updated_fields["category_id"] = command.category_id

            if command.description is not None:
                transaction.update_description(command.description)
                updated_fields["description"] = command.description

            self._uow.transactions.save(transaction)

            # Add domain event
            if updated_fields:
                event = TransactionUpdated(
                    transaction_id=command.transaction_id,
                    user_id=command.user_id,
                    updated_fields=updated_fields,
                )
                self._uow.add_event(event)

    def delete_transaction(self, command: DeleteTransactionCommand) -> None:
        """Delete a transaction."""
        with self._uow:
            transaction = self._uow.transactions.get_by_id(
                TransactionId(command.transaction_id)
            )
            if not transaction:
                raise ValueError("Transaction not found")
            if transaction.user_id.value != command.user_id:
                raise ValueError("Transaction does not belong to user")

            self._uow.transactions.delete(TransactionId(command.transaction_id))

            # Add domain event
            event = TransactionDeleted(
                transaction_id=command.transaction_id,
                user_id=command.user_id,
                transaction_type=transaction.transaction_type.value,
                amount=str(transaction.amount.amount),
            )
            self._uow.add_event(event)

    def get_user_transactions(self, user_id: str) -> List[Transaction]:
        """Get all transactions for a user."""
        return self._uow.transactions.get_by_user_id(UserId(user_id))

    def get_transaction_by_id(
        self, transaction_id: str, user_id: str
    ) -> Optional[Transaction]:
        """Get a transaction by ID, ensuring it belongs to the user."""
        transaction = self._uow.transactions.get_by_id(TransactionId(transaction_id))
        if transaction and transaction.user_id.value == user_id:
            return transaction
        return None
