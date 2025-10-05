"""
Base ApplicationUsecase interface for Clean Architecture.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

# Type variables for request and response
TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")


class ApplicationUsecase(ABC, Generic[TRequest, TResponse]):
    """
    Base interface for application use cases.

    A use case represents a single business operation that can be performed
    by the application. It encapsulates the business logic and orchestrates
    the interaction between domain entities and infrastructure services.

    Type Parameters:
        TRequest: The type of the request object
        TResponse: The type of the response object
    """

    @abstractmethod
    def execute(self, request: TRequest) -> TResponse:
        """
        Execute the use case with the given request.

        Args:
            request: The request object containing input data

        Returns:
            The response object containing the result

        Raises:
            Any domain-specific exceptions that may occur during execution
        """
        pass
