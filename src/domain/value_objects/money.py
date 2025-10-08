from decimal import Decimal
from typing import Union


class Money:
    """Value object representing monetary amounts."""

    def __init__(self, amount: Union[Decimal, float, int], currency: str = "USD"):
        if isinstance(amount, (float, int)):
            amount = Decimal(str(amount))
        elif not isinstance(amount, Decimal):
            raise ValueError("Amount must be a Decimal, float, or int")

        if amount < 0:
            raise ValueError("Amount cannot be negative")

        self._amount = amount.quantize(Decimal("0.01"))
        self._currency = currency.upper()

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def currency(self) -> str:
        return self._currency

    def add(self, other: "Money") -> "Money":
        if self._currency != other._currency:
            raise ValueError("Cannot add different currencies")
        return Money(self._amount + other._amount, self._currency)

    def subtract(self, other: "Money") -> "Money":
        if self._currency != other._currency:
            raise ValueError("Cannot subtract different currencies")
        result_amount = self._amount - other._amount
        if result_amount < 0:
            raise ValueError("Result cannot be negative")
        return Money(result_amount, self._currency)

    def multiply(self, factor: Union[Decimal, float, int]) -> "Money":
        if isinstance(factor, (float, int)):
            factor = Decimal(str(factor))
        return Money(self._amount * factor, self._currency)

    def is_greater_than(self, other: "Money") -> bool:
        if self._currency != other._currency:
            raise ValueError("Cannot compare different currencies")
        return self._amount > other._amount

    def is_equal_to(self, other: "Money") -> bool:
        return self._currency == other._currency and self._amount == other._amount

    def __str__(self) -> str:
        return f"{self._currency} {self._amount:.2f}"

    def __repr__(self) -> str:
        return f"Money({self._amount}, '{self._currency}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Money):
            return False
        return self.is_equal_to(other)

    def __hash__(self) -> int:
        return hash((self._amount, self._currency))
