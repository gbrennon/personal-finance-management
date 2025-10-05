"""
Use cases for Finance application layer.
"""

from decimal import Decimal
from datetime import date

from foundations import ApplicationUsecase
from ..domain.entities import FinanceTransaction, Budget, Category, TransactionType
from .repositories import TransactionRepository, BudgetRepository, CategoryRepository
from .dtos import (
    CreateTransactionRequest,
    CreateTransactionResponse,
    CreateBudgetRequest,
    CreateBudgetResponse,
    GetTransactionsRequest,
    GetTransactionsResponse,
    GetBudgetRequest,
    GetBudgetResponse,
    UpdateTransactionRequest,
    UpdateTransactionResponse,
    DeleteTransactionRequest,
    DeleteTransactionResponse,
    TransactionDto,
    BudgetDto,
)


class CreateTransactionUsecase(
    ApplicationUsecase[CreateTransactionRequest, CreateTransactionResponse]
):
    """
    Use case for creating a new transaction.
    """

    def __init__(
        self,
        transaction_repository: TransactionRepository,
        category_repository: CategoryRepository,
        budget_repository: BudgetRepository,
    ):
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository
        self.budget_repository = budget_repository

    def execute(self, request: CreateTransactionRequest) -> CreateTransactionResponse:
        try:
            # Find the category
            category = self.category_repository.find_by_id(request.category_id)
            if not category:
                return CreateTransactionResponse(
                    transaction_id="", success=False, message="Category not found"
                )

            # Validate category belongs to user
            if category.user_id != request.user_id:
                return CreateTransactionResponse(
                    transaction_id="",
                    success=False,
                    message="Category does not belong to user",
                )

            # Create transaction
            transaction_type = TransactionType(request.transaction_type)
            transaction = FinanceTransaction(
                user_id=request.user_id,
                transaction_type=transaction_type,
                amount=request.amount,
                category=category,
                transaction_date=request.transaction_date,
            )

            # Save transaction
            saved_transaction = self.transaction_repository.save(transaction)

            # Check budget if it's an expense
            if transaction_type == TransactionType.EXPENSE:
                budget = self.budget_repository.find_by_user_and_period(
                    request.user_id,
                    request.transaction_date.month,
                    request.transaction_date.year,
                )

                if budget and budget.amount:
                    total_expenses = (
                        self.transaction_repository.get_total_by_type_and_period(
                            request.user_id,
                            TransactionType.EXPENSE.value,
                            request.transaction_date.month,
                            request.transaction_date.year,
                        )
                    )
                    budget.check_budget_exceeded(total_expenses)
                    self.budget_repository.save(budget)

            return CreateTransactionResponse(
                transaction_id=saved_transaction.id,
                success=True,
                message="Transaction created successfully",
            )

        except Exception as e:
            return CreateTransactionResponse(
                transaction_id="",
                success=False,
                message=f"Error creating transaction: {str(e)}",
            )


class CreateBudgetUsecase(
    ApplicationUsecase[CreateBudgetRequest, CreateBudgetResponse]
):
    """
    Use case for creating or updating a budget.
    """

    def __init__(self, budget_repository: BudgetRepository):
        self.budget_repository = budget_repository

    def execute(self, request: CreateBudgetRequest) -> CreateBudgetResponse:
        try:
            # Check if budget already exists for this period
            existing_budget = self.budget_repository.find_by_user_and_period(
                request.user_id, request.month, request.year
            )

            if existing_budget:
                # Update existing budget
                existing_budget.update_amount(request.amount)
                saved_budget = self.budget_repository.save(existing_budget)
                message = "Budget updated successfully"
            else:
                # Create new budget
                budget = Budget(
                    user_id=request.user_id,
                    amount=request.amount,
                    month=request.month,
                    year=request.year,
                )
                saved_budget = self.budget_repository.save(budget)
                message = "Budget created successfully"

            return CreateBudgetResponse(
                budget_id=saved_budget.id, success=True, message=message
            )

        except Exception as e:
            return CreateBudgetResponse(
                budget_id="", success=False, message=f"Error creating budget: {str(e)}"
            )


class GetTransactionsUsecase(
    ApplicationUsecase[GetTransactionsRequest, GetTransactionsResponse]
):
    """
    Use case for retrieving transactions.
    """

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, request: GetTransactionsRequest) -> GetTransactionsResponse:
        try:
            # Get transactions based on filters
            if request.month and request.year:
                transactions = self.transaction_repository.find_by_user_and_date_range(
                    request.user_id, request.month, request.year
                )
            elif request.transaction_type:
                transactions = self.transaction_repository.find_by_user_and_type(
                    request.user_id, request.transaction_type
                )
            else:
                transactions = self.transaction_repository.find_by_user_id(
                    request.user_id
                )

            # Convert to DTOs
            transaction_dtos = []
            for transaction in transactions:
                dto = TransactionDto(
                    id=transaction.id,
                    user_id=transaction.user_id,
                    transaction_type=transaction.transaction_type.value,
                    amount=float(transaction.amount),
                    category_name=transaction.category.name,
                    category_id=transaction.category.id,
                    transaction_date=transaction.transaction_date.isoformat(),
                    created_at=transaction.created_at.isoformat(),
                    updated_at=transaction.updated_at.isoformat(),
                )
                transaction_dtos.append(dto)

            return GetTransactionsResponse(
                transactions=transaction_dtos,
                total_count=len(transaction_dtos),
                success=True,
                message="Transactions retrieved successfully",
            )

        except Exception as e:
            return GetTransactionsResponse(
                transactions=[],
                total_count=0,
                success=False,
                message=f"Error retrieving transactions: {str(e)}",
            )


class GetBudgetUsecase(ApplicationUsecase[GetBudgetRequest, GetBudgetResponse]):
    """
    Use case for retrieving a budget.
    """

    def __init__(self, budget_repository: BudgetRepository):
        self.budget_repository = budget_repository

    def execute(self, request: GetBudgetRequest) -> GetBudgetResponse:
        try:
            budget = self.budget_repository.find_by_user_and_period(
                request.user_id, request.month, request.year
            )

            budget_dto = None
            if budget:
                budget_dto = BudgetDto(
                    id=budget.id,
                    user_id=budget.user_id,
                    amount=float(budget.amount) if budget.amount else None,
                    month=budget.month,
                    year=budget.year,
                    created_at=budget.created_at.isoformat(),
                    updated_at=budget.updated_at.isoformat(),
                )

            return GetBudgetResponse(
                budget=budget_dto, success=True, message="Budget retrieved successfully"
            )

        except Exception as e:
            return GetBudgetResponse(
                budget=None, success=False, message=f"Error retrieving budget: {str(e)}"
            )


class UpdateTransactionUsecase(
    ApplicationUsecase[UpdateTransactionRequest, UpdateTransactionResponse]
):
    """
    Use case for updating a transaction.
    """

    def __init__(
        self,
        transaction_repository: TransactionRepository,
        category_repository: CategoryRepository,
    ):
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository

    def execute(self, request: UpdateTransactionRequest) -> UpdateTransactionResponse:
        try:
            # Find the transaction
            transaction = self.transaction_repository.find_by_id(request.transaction_id)
            if not transaction:
                return UpdateTransactionResponse(
                    transaction_id=request.transaction_id,
                    success=False,
                    message="Transaction not found",
                )

            # Validate ownership
            if transaction.user_id != request.user_id:
                return UpdateTransactionResponse(
                    transaction_id=request.transaction_id,
                    success=False,
                    message="Transaction does not belong to user",
                )

            # Update fields
            if request.amount:
                transaction.update_amount(request.amount)

            if request.category_id:
                category = self.category_repository.find_by_id(request.category_id)
                if not category:
                    return UpdateTransactionResponse(
                        transaction_id=request.transaction_id,
                        success=False,
                        message="Category not found",
                    )
                transaction.update_category(category)

            # Save transaction
            self.transaction_repository.save(transaction)

            return UpdateTransactionResponse(
                transaction_id=transaction.id,
                success=True,
                message="Transaction updated successfully",
            )

        except Exception as e:
            return UpdateTransactionResponse(
                transaction_id=request.transaction_id,
                success=False,
                message=f"Error updating transaction: {str(e)}",
            )


class DeleteTransactionUsecase(
    ApplicationUsecase[DeleteTransactionRequest, DeleteTransactionResponse]
):
    """
    Use case for deleting a transaction.
    """

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, request: DeleteTransactionRequest) -> DeleteTransactionResponse:
        try:
            # Find the transaction
            transaction = self.transaction_repository.find_by_id(request.transaction_id)
            if not transaction:
                return DeleteTransactionResponse(
                    transaction_id=request.transaction_id,
                    success=False,
                    message="Transaction not found",
                )

            # Validate ownership
            if transaction.user_id != request.user_id:
                return DeleteTransactionResponse(
                    transaction_id=request.transaction_id,
                    success=False,
                    message="Transaction does not belong to user",
                )

            # Delete transaction
            self.transaction_repository.delete(transaction)

            return DeleteTransactionResponse(
                transaction_id=request.transaction_id,
                success=True,
                message="Transaction deleted successfully",
            )

        except Exception as e:
            return DeleteTransactionResponse(
                transaction_id=request.transaction_id,
                success=False,
                message=f"Error deleting transaction: {str(e)}",
            )
