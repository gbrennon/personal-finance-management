from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class CreateBudgetCommand:
    """Command to create a new budget."""

    user_id: str
    month: int
    year: int
    amount: Optional[Decimal] = None


@dataclass
class UpdateBudgetCommand:
    """Command to update an existing budget."""

    budget_id: str
    user_id: str
    amount: Optional[Decimal] = None
