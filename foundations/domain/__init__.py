"""
Domain layer base classes for Clean Architecture.
"""

from .entity import Entity
from .aggregate_root import AggregateRoot
from .aggregate_version import AggregateVersion

__all__ = ["Entity", "AggregateRoot", "AggregateVersion"]
