from dataclasses import dataclass
from datetime import date
from typing import Optional
from decimal import Decimal


@dataclass
class CreateInvestmentCommand:
    """Command to create a new investment."""

    user_id: str
    investment_type: str
    symbol: str
    name: str
    initial_amount: Decimal
    purchase_date: date
    description: Optional[str] = None


@dataclass
class UpdateInvestmentValueCommand:
    """Command to update an investment's current value."""

    investment_id: str
    user_id: str
    new_value: Decimal
