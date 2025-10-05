"""
Django repository implementations for Finance application layer.
"""

from typing import List, Optional
from decimal import Decimal
from django.contrib.auth.models import User
from django.db.models import Sum

from ..application.repositories import (
    TransactionRepository,
    BudgetRepository,
    CategoryRepository,
)
from ..domain.entities import FinanceTransaction, Budget, Category
from ..models import (
    Transaction as DjangoTransaction,
    Budget as DjangoBudget,
    Category as DjangoCategory,
)
from .mappers import TransactionMapper, BudgetMapper, CategoryMapper


class DjangoTransactionRepository(TransactionRepository):
    """
    Django implementation of TransactionRepository.
    """

    def save(self, entity: FinanceTransaction) -> FinanceTransaction:
        """Save a transaction entity."""
        try:
            # Check if entity already has a Django ID (for updates)
            django_transaction = None
            if entity.id and entity.id.isdigit():
                try:
                    django_transaction = DjangoTransaction.objects.get(
                        pk=int(entity.id)
                    )
                    django_transaction = TransactionMapper.to_django(
                        entity, django_transaction
                    )
                except DjangoTransaction.DoesNotExist:
                    django_transaction = TransactionMapper.to_django(entity)
            else:
                django_transaction = TransactionMapper.to_django(entity)

            # Set user and category
            user = User.objects.get(pk=int(entity.user_id))
            category = DjangoCategory.objects.get(pk=int(entity.category.id))

            django_transaction.user = user
            django_transaction.category = category
            django_transaction.save()

            # Create new entity with updated ID if needed
            if not entity.id.isdigit():
                return FinanceTransaction(
                    user_id=entity.user_id,
                    transaction_type=entity.transaction_type,
                    amount=entity.amount,
                    category=entity.category,
                    transaction_date=entity.transaction_date,
                    entity_id=str(django_transaction.pk),
                )

            return entity

        except Exception as e:
            raise Exception(f"Error saving transaction: {str(e)}")

    def find_by_id(self, entity_id: str) -> Optional[FinanceTransaction]:
        """Find a transaction by ID."""
        try:
            django_transaction = DjangoTransaction.objects.get(pk=int(entity_id))
            return TransactionMapper.to_domain(django_transaction)
        except DjangoTransaction.DoesNotExist:
            return None

    def find_all(self) -> List[FinanceTransaction]:
        """Find all transactions."""
        django_transactions = DjangoTransaction.objects.all()
        return [TransactionMapper.to_domain(t) for t in django_transactions]

    def delete(self, entity: FinanceTransaction) -> None:
        """Delete a transaction entity."""
        try:
            django_transaction = DjangoTransaction.objects.get(pk=int(entity.id))
            django_transaction.delete()
        except DjangoTransaction.DoesNotExist:
            pass

    def delete_by_id(self, entity_id: str) -> bool:
        """Delete a transaction by ID."""
        try:
            django_transaction = DjangoTransaction.objects.get(pk=int(entity_id))
            django_transaction.delete()
            return True
        except DjangoTransaction.DoesNotExist:
            return False

    def exists(self, entity_id: str) -> bool:
        """Check if a transaction exists."""
        return DjangoTransaction.objects.filter(pk=int(entity_id)).exists()

    def count(self) -> int:
        """Count total transactions."""
        return DjangoTransaction.objects.count()

    def find_by_user_id(self, user_id: str) -> List[FinanceTransaction]:
        """Find all transactions for a specific user."""
        django_transactions = DjangoTransaction.objects.filter(
            user__pk=int(user_id)
        ).order_by("-date")
        return [TransactionMapper.to_domain(t) for t in django_transactions]

    def find_by_user_and_type(
        self, user_id: str, transaction_type: str
    ) -> List[FinanceTransaction]:
        """Find transactions by user and type."""
        django_transactions = DjangoTransaction.objects.filter(
            user__pk=int(user_id), transaction_type=transaction_type
        ).order_by("-date")
        return [TransactionMapper.to_domain(t) for t in django_transactions]

    def find_by_user_and_date_range(
        self, user_id: str, month: int, year: int
    ) -> List[FinanceTransaction]:
        """Find transactions by user within a specific month/year."""
        django_transactions = DjangoTransaction.objects.filter(
            user__pk=int(user_id), date__month=month, date__year=year
        ).order_by("-date")
        return [TransactionMapper.to_domain(t) for t in django_transactions]

    def get_total_by_type_and_period(
        self, user_id: str, transaction_type: str, month: int, year: int
    ) -> Decimal:
        """Get total amount for a specific transaction type in a given period."""
        result = DjangoTransaction.objects.filter(
            user__pk=int(user_id),
            transaction_type=transaction_type,
            date__month=month,
            date__year=year,
        ).aggregate(total=Sum("amount"))

        return result["total"] or Decimal("0")


class DjangoBudgetRepository(BudgetRepository):
    """
    Django implementation of BudgetRepository.
    """

    def save(self, entity: Budget) -> Budget:
        """Save a budget entity."""
        try:
            # Check if entity already has a Django ID (for updates)
            django_budget = None
            if entity.id and entity.id.isdigit():
                try:
                    django_budget = DjangoBudget.objects.get(pk=int(entity.id))
                    django_budget = BudgetMapper.to_django(entity, django_budget)
                except DjangoBudget.DoesNotExist:
                    django_budget = BudgetMapper.to_django(entity)
            else:
                django_budget = BudgetMapper.to_django(entity)

            # Set user
            user = User.objects.get(pk=int(entity.user_id))
            django_budget.user = user
            django_budget.save()

            # Create new entity with updated ID if needed
            if not entity.id.isdigit():
                return Budget(
                    user_id=entity.user_id,
                    amount=entity.amount,
                    month=entity.month,
                    year=entity.year,
                    entity_id=str(django_budget.pk),
                )

            return entity

        except Exception as e:
            raise Exception(f"Error saving budget: {str(e)}")

    def find_by_id(self, entity_id: str) -> Optional[Budget]:
        """Find a budget by ID."""
        try:
            django_budget = DjangoBudget.objects.get(pk=int(entity_id))
            return BudgetMapper.to_domain(django_budget)
        except DjangoBudget.DoesNotExist:
            return None

    def find_all(self) -> List[Budget]:
        """Find all budgets."""
        django_budgets = DjangoBudget.objects.all()
        return [BudgetMapper.to_domain(b) for b in django_budgets]

    def delete(self, entity: Budget) -> None:
        """Delete a budget entity."""
        try:
            django_budget = DjangoBudget.objects.get(pk=int(entity.id))
            django_budget.delete()
        except DjangoBudget.DoesNotExist:
            pass

    def delete_by_id(self, entity_id: str) -> bool:
        """Delete a budget by ID."""
        try:
            django_budget = DjangoBudget.objects.get(pk=int(entity_id))
            django_budget.delete()
            return True
        except DjangoBudget.DoesNotExist:
            return False

    def exists(self, entity_id: str) -> bool:
        """Check if a budget exists."""
        return DjangoBudget.objects.filter(pk=int(entity_id)).exists()

    def count(self) -> int:
        """Count total budgets."""
        return DjangoBudget.objects.count()

    def find_by_user_and_period(
        self, user_id: str, month: int, year: int
    ) -> Optional[Budget]:
        """Find budget for a specific user and period."""
        try:
            django_budget = DjangoBudget.objects.get(
                user__pk=int(user_id), month=month, year=year
            )
            return BudgetMapper.to_domain(django_budget)
        except DjangoBudget.DoesNotExist:
            return None

    def find_by_user_id(self, user_id: str) -> List[Budget]:
        """Find all budgets for a specific user."""
        django_budgets = DjangoBudget.objects.filter(user__pk=int(user_id))
        return [BudgetMapper.to_domain(b) for b in django_budgets]


class DjangoCategoryRepository(CategoryRepository):
    """
    Django implementation of CategoryRepository.
    """

    def save(self, entity: Category) -> Category:
        """Save a category entity."""
        try:
            # Check if entity already has a Django ID (for updates)
            django_category = None
            if entity.id and entity.id.isdigit():
                try:
                    django_category = DjangoCategory.objects.get(pk=int(entity.id))
                    django_category = CategoryMapper.to_django(entity, django_category)
                except DjangoCategory.DoesNotExist:
                    django_category = CategoryMapper.to_django(entity)
            else:
                django_category = CategoryMapper.to_django(entity)

            # Set user
            user = User.objects.get(pk=int(entity.user_id))
            django_category.user = user
            django_category.save()

            # Create new entity with updated ID if needed
            if not entity.id.isdigit():
                return Category(
                    name=entity.name,
                    transaction_type=entity.transaction_type,
                    user_id=entity.user_id,
                    entity_id=str(django_category.pk),
                )

            return entity

        except Exception as e:
            raise Exception(f"Error saving category: {str(e)}")

    def find_by_id(self, entity_id: str) -> Optional[Category]:
        """Find a category by ID."""
        try:
            django_category = DjangoCategory.objects.get(pk=int(entity_id))
            return CategoryMapper.to_domain(django_category)
        except DjangoCategory.DoesNotExist:
            return None

    def find_all(self) -> List[Category]:
        """Find all categories."""
        django_categories = DjangoCategory.objects.all()
        return [CategoryMapper.to_domain(c) for c in django_categories]

    def delete(self, entity: Category) -> None:
        """Delete a category entity."""
        try:
            django_category = DjangoCategory.objects.get(pk=int(entity.id))
            django_category.delete()
        except DjangoCategory.DoesNotExist:
            pass

    def delete_by_id(self, entity_id: str) -> bool:
        """Delete a category by ID."""
        try:
            django_category = DjangoCategory.objects.get(pk=int(entity_id))
            django_category.delete()
            return True
        except DjangoCategory.DoesNotExist:
            return False

    def exists(self, entity_id: str) -> bool:
        """Check if a category exists."""
        return DjangoCategory.objects.filter(pk=int(entity_id)).exists()

    def count(self) -> int:
        """Count total categories."""
        return DjangoCategory.objects.count()

    def find_by_user_id(self, user_id: str) -> List[Category]:
        """Find all categories for a specific user."""
        django_categories = DjangoCategory.objects.filter(user__pk=int(user_id))
        return [CategoryMapper.to_domain(c) for c in django_categories]

    def find_by_user_and_type(
        self, user_id: str, transaction_type: str
    ) -> List[Category]:
        """Find categories by user and transaction type."""
        django_categories = DjangoCategory.objects.filter(
            user__pk=int(user_id), transaction_type=transaction_type
        )
        return [CategoryMapper.to_domain(c) for c in django_categories]

    def find_by_name_and_user(self, name: str, user_id: str) -> Optional[Category]:
        """Find category by name and user."""
        try:
            django_category = DjangoCategory.objects.get(
                name=name, user__pk=int(user_id)
            )
            return CategoryMapper.to_domain(django_category)
        except DjangoCategory.DoesNotExist:
            return None
