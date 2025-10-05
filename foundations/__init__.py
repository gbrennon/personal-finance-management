"""
Foundations library for Clean Architecture implementation.
"""

from .domain import Entity, AggregateRoot, AggregateVersion
from .application import ApplicationUsecase, Repository

__version__ = "1.0.0"
__all__ = [
    "Entity",
    "AggregateRoot",
    "AggregateVersion",
    "ApplicationUsecase",
    "Repository",
]
