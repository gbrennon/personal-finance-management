from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.retirement_goal import RetirementGoal
from ..value_objects.retirement_goal_id import RetirementGoalId
from ..value_objects.user_id import UserId


class RetirementGoalRepository(ABC):
    """Abstract repository for retirement goal entities."""

    @abstractmethod
    def save(self, goal: RetirementGoal) -> None:
        """Save a retirement goal."""
        pass

    @abstractmethod
    def get_by_id(self, goal_id: RetirementGoalId) -> Optional[RetirementGoal]:
        """Get a retirement goal by its ID."""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: UserId) -> List[RetirementGoal]:
        """Get all retirement goals for a user."""
        pass

    @abstractmethod
    def delete(self, goal_id: RetirementGoalId) -> None:
        """Delete a retirement goal."""
        pass

    @abstractmethod
    def exists(self, goal_id: RetirementGoalId) -> bool:
        """Check if a retirement goal exists."""
        pass
