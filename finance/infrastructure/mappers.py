"""
Mappers for converting between domain entities and Django models.
"""

from decimal import Decimal
from datetime import date
from typing import Optional

from ..domain.entities import FinanceTransaction, Budget, Category, TransactionType
from ..models import (
    Transaction as DjangoTransaction,
    Budget as DjangoBudget,
    Category as DjangoCategory,
)


class CategoryMapper:
    """
    Mapper for Category entity and Django Category model.
    """

    @staticmethod
    def to_domain(django_category: DjangoCategory) -> Category:
        """Convert Django Category model to domain Category entity."""
        return Category(
            name=django_category.name,
            transaction_type=TransactionType(django_category.transaction_type),
            user_id=str(django_category.user.pk),
            entity_id=str(django_category.pk),
        )

    @staticmethod
    def to_django(
        category: Category, django_category: Optional[DjangoCategory] = None
    ) -> DjangoCategory:
        """Convert domain Category entity to Django Category model."""
        if django_category is None:
            django_category = DjangoCategory()

        django_category.name = category.name
        django_category.transaction_type = category.transaction_type.value
        # Note: user will be set by the repository
        return django_category


class TransactionMapper:
    """
    Mapper for FinanceTransaction entity and Django Transaction model.
    """

    @staticmethod
    def to_domain(django_transaction: DjangoTransaction) -> FinanceTransaction:
        """Convert Django Transaction model to domain FinanceTransaction entity."""
        category = CategoryMapper.to_domain(django_transaction.category)

        return FinanceTransaction(
            user_id=str(django_transaction.user.pk),
            transaction_type=TransactionType(django_transaction.transaction_type),
            amount=django_transaction.amount,
            category=category,
            transaction_date=django_transaction.date,
            entity_id=str(django_transaction.pk),
        )

    @staticmethod
    def to_django(
        transaction: FinanceTransaction,
        django_transaction: Optional[DjangoTransaction] = None,
    ) -> DjangoTransaction:
        """Convert domain FinanceTransaction entity to Django Transaction model."""
        if django_transaction is None:
            django_transaction = DjangoTransaction()

        django_transaction.transaction_type = transaction.transaction_type.value
        django_transaction.amount = transaction.amount
        django_transaction.date = transaction.transaction_date
        # Note: user and category will be set by the repository
        return django_transaction


class BudgetMapper:
    """
    Mapper for Budget entity and Django Budget model.
    """

    @staticmethod
    def to_domain(django_budget: DjangoBudget) -> Budget:
        """Convert Django Budget model to domain Budget entity."""
        return Budget(
            user_id=str(django_budget.user.pk),
            amount=django_budget.amount,
            month=django_budget.month,
            year=django_budget.year,
            entity_id=str(django_budget.pk),
        )

    @staticmethod
    def to_django(
        budget: Budget, django_budget: Optional[DjangoBudget] = None
    ) -> DjangoBudget:
        """Convert domain Budget entity to Django Budget model."""
        if django_budget is None:
            django_budget = DjangoBudget()

        django_budget.amount = budget.amount
        django_budget.month = budget.month
        django_budget.year = budget.year
        # Note: user will be set by the repository
        return django_budget
