from typing import Union
import uuid


class CategoryId:
    """Value object representing a category identifier."""

    def __init__(self, value: Union[str, int, uuid.UUID]):
        if isinstance(value, uuid.UUID):
            self._value = str(value)
        elif isinstance(value, (str, int)):
            self._value = str(value)
        else:
            raise ValueError("CategoryId must be a string, int, or UUID")

    @property
    def value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"CategoryId('{self._value}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, CategoryId):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)
