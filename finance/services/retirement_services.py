from typing import List, Optional
from datetime import date
from decimal import Decimal
from finance.domain.entities import RetirementGoal, RetirementContribution
from finance.interfaces.repositories import (
    RetirementGoalRepository,
    RetirementContributionRepository,
)
from finance.interfaces.message_bus import MessageBus


class CreateRetirementGoalService:
    """Service for creating retirement goals"""

    def __init__(
        self,
        retirement_goal_repository: RetirementGoalRepository,
        message_bus: MessageBus,
    ):
        self.retirement_goal_repository = retirement_goal_repository
        self.message_bus = message_bus

    def execute(
        self,
        user_id: int,
        target_amount: Decimal,
        target_date: date,
        monthly_contribution: Decimal,
        current_amount: Optional[Decimal] = None,
    ) -> RetirementGoal:
        """Execute retirement goal creation"""
        if current_amount is None:
            current_amount = Decimal("0")

        # Validate inputs
        if target_amount <= 0:
            raise ValueError("Target amount must be positive")
        if monthly_contribution < 0:
            raise ValueError("Monthly contribution cannot be negative")
        if target_date <= date.today():
            raise ValueError("Target date must be in the future")

        # Create retirement goal entity
        goal = RetirementGoal(
            id=None,
            user_id=user_id,
            target_amount=target_amount,
            target_date=target_date,
            current_amount=current_amount,
            monthly_contribution=monthly_contribution,
            created_at=date.today(),
        )

        # Save goal
        saved_goal = self.retirement_goal_repository.create(goal)

        # Publish event
        self.message_bus.publish(
            "retirement_goal.created",
            {
                "goal_id": saved_goal.id,
                "user_id": user_id,
                "target_amount": float(target_amount),
                "target_date": target_date.isoformat(),
                "monthly_contribution": float(monthly_contribution),
                "current_amount": float(current_amount),
            },
        )

        return saved_goal


class GetUserRetirementGoalsService:
    """Service for retrieving user retirement goals"""

    def __init__(self, retirement_goal_repository: RetirementGoalRepository):
        self.retirement_goal_repository = retirement_goal_repository

    def execute(self, user_id: int) -> List[RetirementGoal]:
        """Execute getting user retirement goals"""
        return self.retirement_goal_repository.get_by_user_id(user_id)


class AddRetirementContributionService:
    """Service for adding retirement contributions"""

    def __init__(
        self,
        retirement_goal_repository: RetirementGoalRepository,
        retirement_contribution_repository: RetirementContributionRepository,
        message_bus: MessageBus,
    ):
        self.retirement_goal_repository = retirement_goal_repository
        self.retirement_contribution_repository = retirement_contribution_repository
        self.message_bus = message_bus

    def execute(
        self,
        user_id: int,
        retirement_goal_id: int,
        amount: Decimal,
        contribution_date: date,
        description: Optional[str] = None,
    ) -> RetirementContribution:
        """Execute adding retirement contribution"""
        # Validate retirement goal exists and belongs to user
        goal = self.retirement_goal_repository.get_by_id(retirement_goal_id)
        if not goal or goal.user_id != user_id:
            raise ValueError("Invalid retirement goal for user")

        # Validate amount
        if amount <= 0:
            raise ValueError("Contribution amount must be positive")

        # Create contribution entity
        contribution = RetirementContribution(
            id=None,
            user_id=user_id,
            retirement_goal_id=retirement_goal_id,
            amount=amount,
            contribution_date=contribution_date,
            description=description,
        )

        # Save contribution
        saved_contribution = self.retirement_contribution_repository.create(
            contribution
        )

        # Update goal's current amount
        updated_goal = RetirementGoal(
            id=goal.id,
            user_id=goal.user_id,
            target_amount=goal.target_amount,
            target_date=goal.target_date,
            current_amount=goal.current_amount + amount,
            monthly_contribution=goal.monthly_contribution,
            created_at=goal.created_at,
        )
        self.retirement_goal_repository.update(updated_goal)

        # Publish event
        self.message_bus.publish(
            "retirement_contribution.added",
            {
                "contribution_id": saved_contribution.id,
                "goal_id": retirement_goal_id,
                "user_id": user_id,
                "amount": float(amount),
                "contribution_date": contribution_date.isoformat(),
                "new_current_amount": float(updated_goal.current_amount),
            },
        )

        return saved_contribution


class GetRetirementContributionsService:
    """Service for retrieving retirement contributions"""

    def __init__(
        self, retirement_contribution_repository: RetirementContributionRepository
    ):
        self.retirement_contribution_repository = retirement_contribution_repository

    def execute(self, user_id: int) -> List[RetirementContribution]:
        """Execute getting user retirement contributions"""
        return self.retirement_contribution_repository.get_by_user_id(user_id)


class GetGoalContributionsService:
    """Service for retrieving contributions for a specific goal"""

    def __init__(
        self,
        retirement_goal_repository: RetirementGoalRepository,
        retirement_contribution_repository: RetirementContributionRepository,
    ):
        self.retirement_goal_repository = retirement_goal_repository
        self.retirement_contribution_repository = retirement_contribution_repository

    def execute(self, user_id: int, goal_id: int) -> List[RetirementContribution]:
        """Execute getting contributions for a specific goal"""
        # Validate goal exists and belongs to user
        goal = self.retirement_goal_repository.get_by_id(goal_id)
        if not goal or goal.user_id != user_id:
            raise ValueError("Invalid retirement goal for user")

        return self.retirement_contribution_repository.get_by_goal_id(goal_id)


class UpdateRetirementGoalService:
    """Service for updating retirement goals"""

    def __init__(
        self,
        retirement_goal_repository: RetirementGoalRepository,
        message_bus: MessageBus,
    ):
        self.retirement_goal_repository = retirement_goal_repository
        self.message_bus = message_bus

    def execute(
        self,
        goal_id: int,
        user_id: int,
        target_amount: Decimal,
        target_date: date,
        monthly_contribution: Decimal,
    ) -> RetirementGoal:
        """Execute retirement goal update"""
        # Get existing goal
        existing_goal = self.retirement_goal_repository.get_by_id(goal_id)
        if not existing_goal or existing_goal.user_id != user_id:
            raise ValueError("Retirement goal not found or access denied")

        # Validate inputs
        if target_amount <= 0:
            raise ValueError("Target amount must be positive")
        if monthly_contribution < 0:
            raise ValueError("Monthly contribution cannot be negative")
        if target_date <= date.today():
            raise ValueError("Target date must be in the future")

        # Update goal entity
        updated_goal = RetirementGoal(
            id=goal_id,
            user_id=user_id,
            target_amount=target_amount,
            target_date=target_date,
            current_amount=existing_goal.current_amount,  # Keep current amount
            monthly_contribution=monthly_contribution,
            created_at=existing_goal.created_at,  # Keep original creation date
        )

        # Save updated goal
        saved_goal = self.retirement_goal_repository.update(updated_goal)

        # Publish event
        self.message_bus.publish(
            "retirement_goal.updated",
            {
                "goal_id": goal_id,
                "user_id": user_id,
                "target_amount": float(target_amount),
                "target_date": target_date.isoformat(),
                "monthly_contribution": float(monthly_contribution),
            },
        )

        return saved_goal
