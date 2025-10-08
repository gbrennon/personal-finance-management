from enum import Enum

from ..value_objects.category_id import CategoryId
from ..value_objects.user_id import UserId


class CategoryType(Enum):
    INCOME = "Income"
    EXPENSE = "Expense"


class Category:
    """Domain entity representing a transaction category."""

    def __init__(
        self,
        category_id: CategoryId,
        user_id: UserId,
        name: str,
        category_type: CategoryType,
    ):
        if not name or not name.strip():
            raise ValueError("Category name cannot be empty")

        self._category_id = category_id
        self._user_id = user_id
        self._name = name.strip()
        self._category_type = category_type

    @property
    def category_id(self) -> CategoryId:
        return self._category_id

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def category_type(self) -> CategoryType:
        return self._category_type

    def update_name(self, new_name: str) -> None:
        """Update the category name."""
        if not new_name or not new_name.strip():
            raise ValueError("Category name cannot be empty")
        self._name = new_name.strip()

    def is_income_category(self) -> bool:
        """Check if this is an income category."""
        return self._category_type == CategoryType.INCOME

    def is_expense_category(self) -> bool:
        """Check if this is an expense category."""
        return self._category_type == CategoryType.EXPENSE

    def __eq__(self, other) -> bool:
        if not isinstance(other, Category):
            return False
        return self._category_id == other._category_id

    def __hash__(self) -> int:
        return hash(self._category_id)

    def __str__(self) -> str:
        return (
            f"Category({self._category_id}, {self._name}, {self._category_type.value})"
        )
