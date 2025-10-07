from dataclasses import dataclass
from decimal import Decimal
from datetime import date
from typing import Optional
from enum import Enum


class TransactionType(Enum):
    INCOME = "Income"
    EXPENSE = "Expense"


class CryptoType(Enum):
    BTC = "BTC"
    ETH = "ETH"


@dataclass
class Transaction:
    id: Optional[int]
    user_id: int
    transaction_type: TransactionType
    amount: Decimal
    category_id: int
    date: date

    def __post_init__(self):
        if isinstance(self.transaction_type, str):
            self.transaction_type = TransactionType(self.transaction_type)


@dataclass
class Category:
    id: Optional[int]
    user_id: int
    name: str
    transaction_type: TransactionType

    def __post_init__(self):
        if isinstance(self.transaction_type, str):
            self.transaction_type = TransactionType(self.transaction_type)


@dataclass
class Budget:
    id: Optional[int]
    user_id: int
    amount: Optional[Decimal]
    month: int
    year: int


@dataclass
class RetirementGoal:
    id: Optional[int]
    user_id: int
    target_amount: Decimal
    target_date: date
    current_amount: Decimal
    monthly_contribution: Decimal
    created_at: date


@dataclass
class RetirementContribution:
    id: Optional[int]
    user_id: int
    retirement_goal_id: int
    amount: Decimal
    contribution_date: date
    description: Optional[str] = None


@dataclass
class CryptoInvestment:
    id: Optional[int]
    user_id: int
    crypto_type: CryptoType
    amount_invested: Decimal
    quantity: Decimal
    purchase_price: Decimal
    purchase_date: date
    current_price: Optional[Decimal] = None

    def __post_init__(self):
        if isinstance(self.crypto_type, str):
            self.crypto_type = CryptoType(self.crypto_type)

    @property
    def current_value(self) -> Optional[Decimal]:
        if self.current_price is not None:
            return self.quantity * self.current_price
        return None

    @property
    def profit_loss(self) -> Optional[Decimal]:
        if self.current_value is not None:
            return self.current_value - self.amount_invested
        return None
