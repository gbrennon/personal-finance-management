from dataclasses import dataclass
from datetime import date
from typing import Optional
from decimal import Decimal


@dataclass
class CreateRetirementGoalCommand:
    """Command to create a new retirement goal."""

    user_id: str
    target_amount: Decimal
    target_date: date
    description: Optional[str] = None


@dataclass
class AddRetirementContributionCommand:
    """Command to add a contribution to a retirement goal."""

    goal_id: str
    user_id: str
    contribution_amount: Decimal
