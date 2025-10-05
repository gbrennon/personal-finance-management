"""
Data Transfer Objects for Finance application layer.
"""

from dataclasses import dataclass
from decimal import Decimal
from datetime import date
from typing import Optional, List, Dict, Any


@dataclass
class CreateTransactionRequest:
    user_id: str
    transaction_type: str
    amount: Decimal
    category_id: str
    transaction_date: date


@dataclass
class CreateTransactionResponse:
    transaction_id: str
    success: bool
    message: str


@dataclass
class CreateBudgetRequest:
    user_id: str
    amount: Optional[Decimal]
    month: int
    year: int


@dataclass
class CreateBudgetResponse:
    budget_id: str
    success: bool
    message: str


@dataclass
class GetTransactionsRequest:
    user_id: str
    transaction_type: Optional[str] = None
    month: Optional[int] = None
    year: Optional[int] = None


@dataclass
class TransactionDto:
    id: str
    user_id: str
    transaction_type: str
    amount: float
    category_name: str
    category_id: str
    transaction_date: str
    created_at: str
    updated_at: str


@dataclass
class GetTransactionsResponse:
    transactions: List[TransactionDto]
    total_count: int
    success: bool
    message: str


@dataclass
class GetBudgetRequest:
    user_id: str
    month: int
    year: int


@dataclass
class BudgetDto:
    id: str
    user_id: str
    amount: Optional[float]
    month: int
    year: int
    created_at: str
    updated_at: str


@dataclass
class GetBudgetResponse:
    budget: Optional[BudgetDto]
    success: bool
    message: str


@dataclass
class UpdateTransactionRequest:
    transaction_id: str
    user_id: str
    amount: Optional[Decimal] = None
    category_id: Optional[str] = None
    transaction_date: Optional[date] = None


@dataclass
class UpdateTransactionResponse:
    transaction_id: str
    success: bool
    message: str


@dataclass
class DeleteTransactionRequest:
    transaction_id: str
    user_id: str


@dataclass
class DeleteTransactionResponse:
    transaction_id: str
    success: bool
    message: str
