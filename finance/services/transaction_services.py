from typing import List, Optional
from datetime import date
from decimal import Decimal
from finance.domain.entities import Transaction, TransactionType
from finance.interfaces.repositories import TransactionRepository, CategoryRepository
from finance.interfaces.message_bus import MessageBus


class RegisterTransactionService:
    """Service for registering new transactions"""

    def __init__(
        self,
        transaction_repository: TransactionRepository,
        category_repository: CategoryRepository,
        message_bus: MessageBus,
    ):
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository
        self.message_bus = message_bus

    def execute(
        self,
        user_id: int,
        transaction_type: TransactionType,
        amount: Decimal,
        category_id: int,
        transaction_date: date,
    ) -> Transaction:
        """Execute the transaction registration"""
        # Validate category exists and belongs to user
        category = self.category_repository.get_by_id(category_id)
        if not category or category.user_id != user_id:
            raise ValueError("Invalid category for user")

        # Validate category type matches transaction type
        if category.transaction_type != transaction_type:
            raise ValueError("Category type does not match transaction type")

        # Create transaction entity
        transaction = Transaction(
            id=None,
            user_id=user_id,
            transaction_type=transaction_type,
            amount=amount,
            category_id=category_id,
            date=transaction_date,
        )

        # Save transaction
        saved_transaction = self.transaction_repository.create(transaction)

        # Publish event
        self.message_bus.publish(
            "transaction.created",
            {
                "transaction_id": saved_transaction.id,
                "user_id": user_id,
                "type": transaction_type.value,
                "amount": float(amount),
                "category_id": category_id,
                "date": transaction_date.isoformat(),
            },
        )

        return saved_transaction


class GetUserTransactionsService:
    """Service for retrieving user transactions"""

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, user_id: int) -> List[Transaction]:
        """Execute getting user transactions"""
        return self.transaction_repository.get_by_user_id(user_id)


class UpdateTransactionService:
    """Service for updating transactions"""

    def __init__(
        self,
        transaction_repository: TransactionRepository,
        category_repository: CategoryRepository,
        message_bus: MessageBus,
    ):
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository
        self.message_bus = message_bus

    def execute(
        self,
        transaction_id: int,
        user_id: int,
        transaction_type: TransactionType,
        amount: Decimal,
        category_id: int,
        transaction_date: date,
    ) -> Transaction:
        """Execute the transaction update"""
        # Get existing transaction
        existing_transaction = self.transaction_repository.get_by_id(transaction_id)
        if not existing_transaction or existing_transaction.user_id != user_id:
            raise ValueError("Transaction not found or access denied")

        # Validate category exists and belongs to user
        category = self.category_repository.get_by_id(category_id)
        if not category or category.user_id != user_id:
            raise ValueError("Invalid category for user")

        # Validate category type matches transaction type
        if category.transaction_type != transaction_type:
            raise ValueError("Category type does not match transaction type")

        # Update transaction entity
        updated_transaction = Transaction(
            id=transaction_id,
            user_id=user_id,
            transaction_type=transaction_type,
            amount=amount,
            category_id=category_id,
            date=transaction_date,
        )

        # Save updated transaction
        saved_transaction = self.transaction_repository.update(updated_transaction)

        # Publish event
        self.message_bus.publish(
            "transaction.updated",
            {
                "transaction_id": transaction_id,
                "user_id": user_id,
                "type": transaction_type.value,
                "amount": float(amount),
                "category_id": category_id,
                "date": transaction_date.isoformat(),
            },
        )

        return saved_transaction


class DeleteTransactionService:
    """Service for deleting transactions"""

    def __init__(
        self, transaction_repository: TransactionRepository, message_bus: MessageBus
    ):
        self.transaction_repository = transaction_repository
        self.message_bus = message_bus

    def execute(self, transaction_id: int, user_id: int) -> bool:
        """Execute the transaction deletion"""
        # Get existing transaction to verify ownership
        existing_transaction = self.transaction_repository.get_by_id(transaction_id)
        if not existing_transaction or existing_transaction.user_id != user_id:
            raise ValueError("Transaction not found or access denied")

        # Delete transaction
        success = self.transaction_repository.delete(transaction_id)

        if success:
            # Publish event
            self.message_bus.publish(
                "transaction.deleted",
                {
                    "transaction_id": transaction_id,
                    "user_id": user_id,
                },
            )

        return success
