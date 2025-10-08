from datetime import date
from enum import Enum
from typing import Optional

from ..value_objects.money import Money
from ..value_objects.investment_id import InvestmentId
from ..value_objects.user_id import UserId


class InvestmentType(Enum):
    STOCKS = "Stocks"
    BONDS = "Bonds"
    MUTUAL_FUNDS = "Mutual Funds"
    ETF = "ETF"
    CRYPTOCURRENCY = "Cryptocurrency"
    REAL_ESTATE = "Real Estate"
    COMMODITIES = "Commodities"
    OTHER = "Other"


class Investment:
    """Domain entity representing an investment."""

    def __init__(
        self,
        investment_id: InvestmentId,
        user_id: UserId,
        investment_type: InvestmentType,
        symbol: str,
        name: str,
        initial_amount: Money,
        purchase_date: date,
        current_value: Optional[Money] = None,
        description: Optional[str] = None,
    ):
        if not symbol or not symbol.strip():
            raise ValueError("Investment symbol cannot be empty")
        if not name or not name.strip():
            raise ValueError("Investment name cannot be empty")

        self._investment_id = investment_id
        self._user_id = user_id
        self._investment_type = investment_type
        self._symbol = symbol.strip().upper()
        self._name = name.strip()
        self._initial_amount = initial_amount
        self._purchase_date = purchase_date
        self._current_value = current_value or initial_amount
        self._description = description

    @property
    def investment_id(self) -> InvestmentId:
        return self._investment_id

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def investment_type(self) -> InvestmentType:
        return self._investment_type

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def name(self) -> str:
        return self._name

    @property
    def initial_amount(self) -> Money:
        return self._initial_amount

    @property
    def purchase_date(self) -> date:
        return self._purchase_date

    @property
    def current_value(self) -> Money:
        return self._current_value

    @property
    def description(self) -> Optional[str]:
        return self._description

    def update_current_value(self, new_value: Money) -> None:
        """Update the current value of the investment."""
        if new_value.amount < 0:
            raise ValueError("Investment value cannot be negative")
        self._current_value = new_value

    def update_name(self, new_name: str) -> None:
        """Update the investment name."""
        if not new_name or not new_name.strip():
            raise ValueError("Investment name cannot be empty")
        self._name = new_name.strip()

    def update_description(self, description: Optional[str]) -> None:
        """Update the investment description."""
        self._description = description

    def gain_loss_amount(self) -> Money:
        """Calculate the gain or loss amount."""
        try:
            if self._current_value.is_greater_than(self._initial_amount):
                return self._current_value.subtract(self._initial_amount)
            else:
                return self._initial_amount.subtract(self._current_value)
        except ValueError:
            return Money(0)

    def gain_loss_percentage(self) -> float:
        """Calculate the gain or loss percentage."""
        if self._initial_amount.amount == 0:
            return 0.0

        from decimal import Decimal

        gain_loss = self.gain_loss_amount()
        percentage = (gain_loss.amount / self._initial_amount.amount) * Decimal("100")

        if self._current_value.is_greater_than(self._initial_amount):
            return float(percentage)
        else:
            return float(-percentage)

    def is_profitable(self) -> bool:
        """Check if the investment is currently profitable."""
        return self._current_value.is_greater_than(self._initial_amount)

    def is_loss(self) -> bool:
        """Check if the investment is currently at a loss."""
        return self._initial_amount.is_greater_than(self._current_value)

    def days_held(self) -> int:
        """Calculate the number of days the investment has been held."""
        return (date.today() - self._purchase_date).days

    def __eq__(self, other) -> bool:
        if not isinstance(other, Investment):
            return False
        return self._investment_id == other._investment_id

    def __hash__(self) -> int:
        return hash(self._investment_id)

    def __str__(self) -> str:
        return (
            f"Investment({self._investment_id}, {self._symbol}, {self._current_value})"
        )
