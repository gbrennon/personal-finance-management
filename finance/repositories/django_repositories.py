from typing import List, Optional
from decimal import Decimal
from finance.interfaces.repositories import (
    TransactionRepository,
    CategoryRepository,
    BudgetRepository,
    RetirementGoalRepository,
    RetirementContributionRepository,
    CryptoInvestmentRepository,
)
from finance.domain.entities import (
    Transaction as TransactionEntity,
    Category as CategoryEntity,
    Budget as BudgetEntity,
    RetirementGoal as RetirementGoalEntity,
    RetirementContribution as RetirementContributionEntity,
    CryptoInvestment as CryptoInvestmentEntity,
    TransactionType,
    CryptoType,
)
from finance.models import (
    Transaction as TransactionModel,
    Category as CategoryModel,
    Budget as BudgetModel,
    RetirementGoal as RetirementGoalModel,
    RetirementContribution as RetirementContributionModel,
    CryptoInvestment as CryptoInvestmentModel,
)


class DjangoTransactionRepository(TransactionRepository):
    """Django ORM implementation of TransactionRepository"""

    def _model_to_entity(self, model: TransactionModel) -> TransactionEntity:
        """Convert Django model to domain entity"""
        return TransactionEntity(
            id=model.id,
            user_id=model.user_id,
            transaction_type=TransactionType(model.transaction_type),
            amount=model.amount,
            category_id=model.category_id,
            date=model.date,
        )

    def _entity_to_model_data(self, entity: TransactionEntity) -> dict:
        """Convert domain entity to Django model data"""
        return {
            "user_id": entity.user_id,
            "transaction_type": entity.transaction_type.value,
            "amount": entity.amount,
            "category_id": entity.category_id,
            "date": entity.date,
        }

    def create(self, transaction: TransactionEntity) -> TransactionEntity:
        """Create a new transaction"""
        model_data = self._entity_to_model_data(transaction)
        model = TransactionModel.objects.create(**model_data)
        return self._model_to_entity(model)

    def get_by_id(self, transaction_id: int) -> Optional[TransactionEntity]:
        """Get transaction by ID"""
        try:
            model = TransactionModel.objects.get(id=transaction_id)
            return self._model_to_entity(model)
        except TransactionModel.DoesNotExist:
            return None

    def get_by_user_id(self, user_id: int) -> List[TransactionEntity]:
        """Get all transactions for a user"""
        models = TransactionModel.objects.filter(user_id=user_id).order_by("-date")
        return [self._model_to_entity(model) for model in models]

    def update(self, transaction: TransactionEntity) -> TransactionEntity:
        """Update an existing transaction"""
        model_data = self._entity_to_model_data(transaction)
        TransactionModel.objects.filter(id=transaction.id).update(**model_data)
        model = TransactionModel.objects.get(id=transaction.id)
        return self._model_to_entity(model)

    def delete(self, transaction_id: int) -> bool:
        """Delete a transaction"""
        try:
            TransactionModel.objects.get(id=transaction_id).delete()
            return True
        except TransactionModel.DoesNotExist:
            return False


class DjangoCategoryRepository(CategoryRepository):
    """Django ORM implementation of CategoryRepository"""

    def _model_to_entity(self, model: CategoryModel) -> CategoryEntity:
        """Convert Django model to domain entity"""
        return CategoryEntity(
            id=model.id,
            user_id=model.user_id,
            name=model.name,
            transaction_type=TransactionType(model.transaction_type),
        )

    def _entity_to_model_data(self, entity: CategoryEntity) -> dict:
        """Convert domain entity to Django model data"""
        return {
            "user_id": entity.user_id,
            "name": entity.name,
            "transaction_type": entity.transaction_type.value,
        }

    def create(self, category: CategoryEntity) -> CategoryEntity:
        """Create a new category"""
        model_data = self._entity_to_model_data(category)
        model = CategoryModel.objects.create(**model_data)
        return self._model_to_entity(model)

    def get_by_id(self, category_id: int) -> Optional[CategoryEntity]:
        """Get category by ID"""
        try:
            model = CategoryModel.objects.get(id=category_id)
            return self._model_to_entity(model)
        except CategoryModel.DoesNotExist:
            return None

    def get_by_user_id(self, user_id: int) -> List[CategoryEntity]:
        """Get all categories for a user"""
        models = CategoryModel.objects.filter(user_id=user_id)
        return [self._model_to_entity(model) for model in models]

    def get_by_user_and_type(
        self, user_id: int, transaction_type: str
    ) -> List[CategoryEntity]:
        """Get categories by user and transaction type"""
        models = CategoryModel.objects.filter(
            user_id=user_id, transaction_type=transaction_type
        )
        return [self._model_to_entity(model) for model in models]

    def update(self, category: CategoryEntity) -> CategoryEntity:
        """Update an existing category"""
        model_data = self._entity_to_model_data(category)
        CategoryModel.objects.filter(id=category.id).update(**model_data)
        model = CategoryModel.objects.get(id=category.id)
        return self._model_to_entity(model)

    def delete(self, category_id: int) -> bool:
        """Delete a category"""
        try:
            CategoryModel.objects.get(id=category_id).delete()
            return True
        except CategoryModel.DoesNotExist:
            return False


class DjangoBudgetRepository(BudgetRepository):
    """Django ORM implementation of BudgetRepository"""

    def _model_to_entity(self, model: BudgetModel) -> BudgetEntity:
        """Convert Django model to domain entity"""
        return BudgetEntity(
            id=model.id,
            user_id=model.user_id,
            amount=model.amount,
            month=model.month,
            year=model.year,
        )

    def _entity_to_model_data(self, entity: BudgetEntity) -> dict:
        """Convert domain entity to Django model data"""
        return {
            "user_id": entity.user_id,
            "amount": entity.amount,
            "month": entity.month,
            "year": entity.year,
        }

    def create(self, budget: BudgetEntity) -> BudgetEntity:
        """Create a new budget"""
        model_data = self._entity_to_model_data(budget)
        model = BudgetModel.objects.create(**model_data)
        return self._model_to_entity(model)

    def get_by_id(self, budget_id: int) -> Optional[BudgetEntity]:
        """Get budget by ID"""
        try:
            model = BudgetModel.objects.get(id=budget_id)
            return self._model_to_entity(model)
        except BudgetModel.DoesNotExist:
            return None

    def get_by_user_and_period(
        self, user_id: int, month: int, year: int
    ) -> Optional[BudgetEntity]:
        """Get budget by user and period"""
        try:
            model = BudgetModel.objects.get(user_id=user_id, month=month, year=year)
            return self._model_to_entity(model)
        except BudgetModel.DoesNotExist:
            return None

    def get_by_user_id(self, user_id: int) -> List[BudgetEntity]:
        """Get all budgets for a user"""
        models = BudgetModel.objects.filter(user_id=user_id)
        return [self._model_to_entity(model) for model in models]

    def update(self, budget: BudgetEntity) -> BudgetEntity:
        """Update an existing budget"""
        model_data = self._entity_to_model_data(budget)
        BudgetModel.objects.filter(id=budget.id).update(**model_data)
        model = BudgetModel.objects.get(id=budget.id)
        return self._model_to_entity(model)

    def delete(self, budget_id: int) -> bool:
        """Delete a budget"""
        try:
            BudgetModel.objects.get(id=budget_id).delete()
            return True
        except BudgetModel.DoesNotExist:
            return False


class DjangoRetirementGoalRepository(RetirementGoalRepository):
    """Django ORM implementation of RetirementGoalRepository"""

    def _model_to_entity(self, model: RetirementGoalModel) -> RetirementGoalEntity:
        """Convert Django model to domain entity"""
        return RetirementGoalEntity(
            id=model.id,
            user_id=model.user_id,
            target_amount=model.target_amount,
            target_date=model.target_date,
            current_amount=model.current_amount,
            monthly_contribution=model.monthly_contribution,
            created_at=model.created_at,
        )

    def _entity_to_model_data(self, entity: RetirementGoalEntity) -> dict:
        """Convert domain entity to Django model data"""
        return {
            "user_id": entity.user_id,
            "target_amount": entity.target_amount,
            "target_date": entity.target_date,
            "current_amount": entity.current_amount,
            "monthly_contribution": entity.monthly_contribution,
            "created_at": entity.created_at,
        }

    def create(self, goal: RetirementGoalEntity) -> RetirementGoalEntity:
        """Create a new retirement goal"""
        model_data = self._entity_to_model_data(goal)
        model = RetirementGoalModel.objects.create(**model_data)
        return self._model_to_entity(model)

    def get_by_id(self, goal_id: int) -> Optional[RetirementGoalEntity]:
        """Get retirement goal by ID"""
        try:
            model = RetirementGoalModel.objects.get(id=goal_id)
            return self._model_to_entity(model)
        except RetirementGoalModel.DoesNotExist:
            return None

    def get_by_user_id(self, user_id: int) -> List[RetirementGoalEntity]:
        """Get all retirement goals for a user"""
        models = RetirementGoalModel.objects.filter(user_id=user_id)
        return [self._model_to_entity(model) for model in models]

    def update(self, goal: RetirementGoalEntity) -> RetirementGoalEntity:
        """Update an existing retirement goal"""
        model_data = self._entity_to_model_data(goal)
        RetirementGoalModel.objects.filter(id=goal.id).update(**model_data)
        model = RetirementGoalModel.objects.get(id=goal.id)
        return self._model_to_entity(model)

    def delete(self, goal_id: int) -> bool:
        """Delete a retirement goal"""
        try:
            RetirementGoalModel.objects.get(id=goal_id).delete()
            return True
        except RetirementGoalModel.DoesNotExist:
            return False


class DjangoRetirementContributionRepository(RetirementContributionRepository):
    """Django ORM implementation of RetirementContributionRepository"""

    def _model_to_entity(
        self, model: RetirementContributionModel
    ) -> RetirementContributionEntity:
        """Convert Django model to domain entity"""
        return RetirementContributionEntity(
            id=model.id,
            user_id=model.user_id,
            retirement_goal_id=model.retirement_goal_id,
            amount=model.amount,
            contribution_date=model.contribution_date,
            description=model.description,
        )

    def _entity_to_model_data(self, entity: RetirementContributionEntity) -> dict:
        """Convert domain entity to Django model data"""
        return {
            "user_id": entity.user_id,
            "retirement_goal_id": entity.retirement_goal_id,
            "amount": entity.amount,
            "contribution_date": entity.contribution_date,
            "description": entity.description,
        }

    def create(
        self, contribution: RetirementContributionEntity
    ) -> RetirementContributionEntity:
        """Create a new retirement contribution"""
        model_data = self._entity_to_model_data(contribution)
        model = RetirementContributionModel.objects.create(**model_data)
        return self._model_to_entity(model)

    def get_by_id(self, contribution_id: int) -> Optional[RetirementContributionEntity]:
        """Get retirement contribution by ID"""
        try:
            model = RetirementContributionModel.objects.get(id=contribution_id)
            return self._model_to_entity(model)
        except RetirementContributionModel.DoesNotExist:
            return None

    def get_by_user_id(self, user_id: int) -> List[RetirementContributionEntity]:
        """Get all retirement contributions for a user"""
        models = RetirementContributionModel.objects.filter(user_id=user_id)
        return [self._model_to_entity(model) for model in models]

    def get_by_goal_id(self, goal_id: int) -> List[RetirementContributionEntity]:
        """Get all contributions for a specific retirement goal"""
        models = RetirementContributionModel.objects.filter(retirement_goal_id=goal_id)
        return [self._model_to_entity(model) for model in models]

    def update(
        self, contribution: RetirementContributionEntity
    ) -> RetirementContributionEntity:
        """Update an existing retirement contribution"""
        model_data = self._entity_to_model_data(contribution)
        RetirementContributionModel.objects.filter(id=contribution.id).update(
            **model_data
        )
        model = RetirementContributionModel.objects.get(id=contribution.id)
        return self._model_to_entity(model)

    def delete(self, contribution_id: int) -> bool:
        """Delete a retirement contribution"""
        try:
            RetirementContributionModel.objects.get(id=contribution_id).delete()
            return True
        except RetirementContributionModel.DoesNotExist:
            return False


class DjangoCryptoInvestmentRepository(CryptoInvestmentRepository):
    """Django ORM implementation of CryptoInvestmentRepository"""

    def _model_to_entity(self, model: CryptoInvestmentModel) -> CryptoInvestmentEntity:
        """Convert Django model to domain entity"""
        return CryptoInvestmentEntity(
            id=model.id,
            user_id=model.user_id,
            crypto_type=CryptoType(model.crypto_type),
            amount_invested=model.amount_invested,
            quantity=model.quantity,
            purchase_price=model.purchase_price,
            purchase_date=model.purchase_date,
            current_price=model.current_price,
        )

    def _entity_to_model_data(self, entity: CryptoInvestmentEntity) -> dict:
        """Convert domain entity to Django model data"""
        return {
            "user_id": entity.user_id,
            "crypto_type": entity.crypto_type.value,
            "amount_invested": entity.amount_invested,
            "quantity": entity.quantity,
            "purchase_price": entity.purchase_price,
            "purchase_date": entity.purchase_date,
            "current_price": entity.current_price,
        }

    def create(self, investment: CryptoInvestmentEntity) -> CryptoInvestmentEntity:
        """Create a new crypto investment"""
        model_data = self._entity_to_model_data(investment)
        model = CryptoInvestmentModel.objects.create(**model_data)
        return self._model_to_entity(model)

    def get_by_id(self, investment_id: int) -> Optional[CryptoInvestmentEntity]:
        """Get crypto investment by ID"""
        try:
            model = CryptoInvestmentModel.objects.get(id=investment_id)
            return self._model_to_entity(model)
        except CryptoInvestmentModel.DoesNotExist:
            return None

    def get_by_user_id(self, user_id: int) -> List[CryptoInvestmentEntity]:
        """Get all crypto investments for a user"""
        models = CryptoInvestmentModel.objects.filter(user_id=user_id)
        return [self._model_to_entity(model) for model in models]

    def get_by_user_and_crypto_type(
        self, user_id: int, crypto_type: str
    ) -> List[CryptoInvestmentEntity]:
        """Get crypto investments by user and crypto type"""
        models = CryptoInvestmentModel.objects.filter(
            user_id=user_id, crypto_type=crypto_type
        )
        return [self._model_to_entity(model) for model in models]

    def update(self, investment: CryptoInvestmentEntity) -> CryptoInvestmentEntity:
        """Update an existing crypto investment"""
        model_data = self._entity_to_model_data(investment)
        CryptoInvestmentModel.objects.filter(id=investment.id).update(**model_data)
        model = CryptoInvestmentModel.objects.get(id=investment.id)
        return self._model_to_entity(model)

    def delete(self, investment_id: int) -> bool:
        """Delete a crypto investment"""
        try:
            CryptoInvestmentModel.objects.get(id=investment_id).delete()
            return True
        except CryptoInvestmentModel.DoesNotExist:
            return False
