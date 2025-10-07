from abc import ABC, abstractmethod
from typing import List, Optional
from finance.domain.entities import (
    Transaction,
    Category,
    Budget,
    RetirementGoal,
    RetirementContribution,
    CryptoInvestment,
)


class TransactionRepository(ABC):
    """Abstract interface for transaction repository operations"""

    @abstractmethod
    def create(self, transaction: Transaction) -> Transaction:
        """Create a new transaction"""
        pass

    @abstractmethod
    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Get transaction by ID"""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[Transaction]:
        """Get all transactions for a user"""
        pass

    @abstractmethod
    def update(self, transaction: Transaction) -> Transaction:
        """Update an existing transaction"""
        pass

    @abstractmethod
    def delete(self, transaction_id: int) -> bool:
        """Delete a transaction"""
        pass


class CategoryRepository(ABC):
    """Abstract interface for category repository operations"""

    @abstractmethod
    def create(self, category: Category) -> Category:
        """Create a new category"""
        pass

    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID"""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[Category]:
        """Get all categories for a user"""
        pass

    @abstractmethod
    def get_by_user_and_type(
        self, user_id: int, transaction_type: str
    ) -> List[Category]:
        """Get categories by user and transaction type"""
        pass

    @abstractmethod
    def update(self, category: Category) -> Category:
        """Update an existing category"""
        pass

    @abstractmethod
    def delete(self, category_id: int) -> bool:
        """Delete a category"""
        pass


class BudgetRepository(ABC):
    """Abstract interface for budget repository operations"""

    @abstractmethod
    def create(self, budget: Budget) -> Budget:
        """Create a new budget"""
        pass

    @abstractmethod
    def get_by_id(self, budget_id: int) -> Optional[Budget]:
        """Get budget by ID"""
        pass

    @abstractmethod
    def get_by_user_and_period(
        self, user_id: int, month: int, year: int
    ) -> Optional[Budget]:
        """Get budget by user and period"""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[Budget]:
        """Get all budgets for a user"""
        pass

    @abstractmethod
    def update(self, budget: Budget) -> Budget:
        """Update an existing budget"""
        pass

    @abstractmethod
    def delete(self, budget_id: int) -> bool:
        """Delete a budget"""
        pass


class RetirementGoalRepository(ABC):
    """Abstract interface for retirement goal repository operations"""

    @abstractmethod
    def create(self, goal: RetirementGoal) -> RetirementGoal:
        """Create a new retirement goal"""
        pass

    @abstractmethod
    def get_by_id(self, goal_id: int) -> Optional[RetirementGoal]:
        """Get retirement goal by ID"""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[RetirementGoal]:
        """Get all retirement goals for a user"""
        pass

    @abstractmethod
    def update(self, goal: RetirementGoal) -> RetirementGoal:
        """Update an existing retirement goal"""
        pass

    @abstractmethod
    def delete(self, goal_id: int) -> bool:
        """Delete a retirement goal"""
        pass


class RetirementContributionRepository(ABC):
    """Abstract interface for retirement contribution repository operations"""

    @abstractmethod
    def create(self, contribution: RetirementContribution) -> RetirementContribution:
        """Create a new retirement contribution"""
        pass

    @abstractmethod
    def get_by_id(self, contribution_id: int) -> Optional[RetirementContribution]:
        """Get retirement contribution by ID"""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[RetirementContribution]:
        """Get all retirement contributions for a user"""
        pass

    @abstractmethod
    def get_by_goal_id(self, goal_id: int) -> List[RetirementContribution]:
        """Get all contributions for a specific retirement goal"""
        pass

    @abstractmethod
    def update(self, contribution: RetirementContribution) -> RetirementContribution:
        """Update an existing retirement contribution"""
        pass

    @abstractmethod
    def delete(self, contribution_id: int) -> bool:
        """Delete a retirement contribution"""
        pass


class CryptoInvestmentRepository(ABC):
    """Abstract interface for crypto investment repository operations"""

    @abstractmethod
    def create(self, investment: CryptoInvestment) -> CryptoInvestment:
        """Create a new crypto investment"""
        pass

    @abstractmethod
    def get_by_id(self, investment_id: int) -> Optional[CryptoInvestment]:
        """Get crypto investment by ID"""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[CryptoInvestment]:
        """Get all crypto investments for a user"""
        pass

    @abstractmethod
    def get_by_user_and_crypto_type(
        self, user_id: int, crypto_type: str
    ) -> List[CryptoInvestment]:
        """Get crypto investments by user and crypto type"""
        pass

    @abstractmethod
    def update(self, investment: CryptoInvestment) -> CryptoInvestment:
        """Update an existing crypto investment"""
        pass

    @abstractmethod
    def delete(self, investment_id: int) -> bool:
        """Delete a crypto investment"""
        pass
