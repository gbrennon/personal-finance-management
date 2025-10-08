from typing import Any, Dict, Optional
from .base import DomainEvent


class RetirementGoalCreated(DomainEvent):
    """Event raised when a retirement goal is created."""

    def __init__(
        self,
        goal_id: str,
        user_id: str,
        target_amount: str,
        target_date: str,
        description: Optional[str] = None,
    ):
        event_data = {
            "goal_id": goal_id,
            "user_id": user_id,
            "target_amount": target_amount,
            "target_date": target_date,
            "description": description,
        }
        super().__init__(event_data)


class RetirementContributionAdded(DomainEvent):
    """Event raised when a contribution is added to a retirement goal."""

    def __init__(
        self,
        goal_id: str,
        user_id: str,
        contribution_amount: str,
        new_current_amount: str,
    ):
        event_data = {
            "goal_id": goal_id,
            "user_id": user_id,
            "contribution_amount": contribution_amount,
            "new_current_amount": new_current_amount,
        }
        super().__init__(event_data)


class RetirementGoalReached(DomainEvent):
    """Event raised when a retirement goal is reached."""

    def __init__(
        self,
        goal_id: str,
        user_id: str,
        target_amount: str,
        final_amount: str,
        days_to_reach: int,
    ):
        event_data = {
            "goal_id": goal_id,
            "user_id": user_id,
            "target_amount": target_amount,
            "final_amount": final_amount,
            "days_to_reach": days_to_reach,
        }
        super().__init__(event_data)
