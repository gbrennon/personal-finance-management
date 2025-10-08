from typing import List, Optional
import uuid

from ...domain.entities.retirement_goal import RetirementGoal
from ...domain.value_objects.money import Money
from ...domain.value_objects.retirement_goal_id import RetirementGoalId
from ...domain.value_objects.user_id import UserId
from ...domain.events.retirement_events import (
    RetirementGoalCreated,
    RetirementContributionAdded,
    RetirementGoalReached,
)
from ...domain.repositories.unit_of_work import UnitOfWork
from ..commands.retirement_commands import (
    CreateRetirementGoalCommand,
    AddRetirementContributionCommand,
)


class RetirementService:
    """Application service for retirement goal operations."""

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def create_retirement_goal(self, command: CreateRetirementGoalCommand) -> str:
        """Create a new retirement goal."""
        with self._uow:
            goal_id = RetirementGoalId(str(uuid.uuid4()))

            goal = RetirementGoal(
                goal_id=goal_id,
                user_id=UserId(command.user_id),
                target_amount=Money(command.target_amount),
                target_date=command.target_date,
                description=command.description,
            )

            self._uow.retirement_goals.save(goal)

            # Add domain event
            event = RetirementGoalCreated(
                goal_id=goal_id.value,
                user_id=command.user_id,
                target_amount=str(command.target_amount),
                target_date=command.target_date.isoformat(),
                description=command.description,
            )
            self._uow.add_event(event)

            return goal_id.value

    def add_contribution(self, command: AddRetirementContributionCommand) -> None:
        """Add a contribution to a retirement goal."""
        with self._uow:
            goal = self._uow.retirement_goals.get_by_id(
                RetirementGoalId(command.goal_id)
            )
            if not goal:
                raise ValueError("Retirement goal not found")
            if goal.user_id.value != command.user_id:
                raise ValueError("Retirement goal does not belong to user")

            old_amount = goal.current_amount
            goal.add_contribution(Money(command.contribution_amount))

            self._uow.retirement_goals.save(goal)

            # Add domain event
            event = RetirementContributionAdded(
                goal_id=command.goal_id,
                user_id=command.user_id,
                contribution_amount=str(command.contribution_amount),
                new_current_amount=str(goal.current_amount.amount),
            )
            self._uow.add_event(event)

            # Check if goal is reached
            if goal.is_goal_reached() and not old_amount.is_greater_than(
                goal.target_amount
            ):
                goal_reached_event = RetirementGoalReached(
                    goal_id=command.goal_id,
                    user_id=command.user_id,
                    target_amount=str(goal.target_amount.amount),
                    final_amount=str(goal.current_amount.amount),
                    days_to_reach=goal.days_until_target(),
                )
                self._uow.add_event(goal_reached_event)

    def get_user_retirement_goals(self, user_id: str) -> List[RetirementGoal]:
        """Get all retirement goals for a user."""
        return self._uow.retirement_goals.get_by_user_id(UserId(user_id))

    def get_retirement_goal_by_id(
        self, goal_id: str, user_id: str
    ) -> Optional[RetirementGoal]:
        """Get a retirement goal by ID, ensuring it belongs to the user."""
        goal = self._uow.retirement_goals.get_by_id(RetirementGoalId(goal_id))
        if goal and goal.user_id.value == user_id:
            return goal
        return None

    def calculate_monthly_savings_needed(
        self, goal_id: str, user_id: str
    ) -> Optional[Money]:
        """Calculate monthly savings needed to reach a retirement goal."""
        goal = self.get_retirement_goal_by_id(goal_id, user_id)
        if not goal:
            return None
        return goal.monthly_savings_needed()

    def get_retirement_progress(self, goal_id: str, user_id: str) -> Optional[dict]:
        """Get retirement goal progress information."""
        goal = self.get_retirement_goal_by_id(goal_id, user_id)
        if not goal:
            return None

        return {
            "goal_id": goal_id,
            "target_amount": goal.target_amount.amount,
            "current_amount": goal.current_amount.amount,
            "progress_percentage": goal.progress_percentage(),
            "remaining_amount": goal.remaining_amount().amount,
            "days_until_target": goal.days_until_target(),
            "monthly_savings_needed": goal.monthly_savings_needed().amount,
            "is_goal_reached": goal.is_goal_reached(),
        }
