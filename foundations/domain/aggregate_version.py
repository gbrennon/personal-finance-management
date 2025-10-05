"""
AggregateVersion class for tracking aggregate state versions.
"""

from typing import Dict, Any, Optional
from datetime import datetime


class AggregateVersion:
    """
    Represents a specific version of an aggregate's state.

    This class is used for optimistic concurrency control and event sourcing,
    allowing us to track different versions of an aggregate over time.
    """

    def __init__(
        self,
        aggregate_id: str,
        version: int,
        aggregate_type: str,
        data: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
    ):
        """
        Initialize an aggregate version.

        Args:
            aggregate_id: The unique identifier of the aggregate
            version: The version number of this aggregate state
            aggregate_type: The type/class name of the aggregate
            data: The serialized state data of the aggregate at this version
            timestamp: When this version was created (defaults to current time)
        """
        self.aggregate_id = aggregate_id
        self.version = version
        self.aggregate_type = aggregate_type
        self.data = data or {}
        self.timestamp = timestamp or datetime.utcnow()

    def is_newer_than(self, other: "AggregateVersion") -> bool:
        """
        Check if this version is newer than another version.

        Args:
            other: Another aggregate version to compare against

        Returns:
            True if this version is newer, False otherwise
        """
        if self.aggregate_id != other.aggregate_id:
            raise ValueError("Cannot compare versions of different aggregates")

        return self.version > other.version

    def is_same_version(self, other: "AggregateVersion") -> bool:
        """
        Check if this version is the same as another version.

        Args:
            other: Another aggregate version to compare against

        Returns:
            True if versions are the same, False otherwise
        """
        if self.aggregate_id != other.aggregate_id:
            return False

        return self.version == other.version

    def get_next_version(self) -> "AggregateVersion":
        """
        Create a new version instance with incremented version number.

        Returns:
            A new AggregateVersion instance with version + 1
        """
        return AggregateVersion(
            aggregate_id=self.aggregate_id,
            version=self.version + 1,
            aggregate_type=self.aggregate_type,
            data=self.data.copy(),
            timestamp=datetime.utcnow(),
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the aggregate version to a dictionary representation.

        Returns:
            Dictionary representation of the aggregate version
        """
        return {
            "aggregate_id": self.aggregate_id,
            "version": self.version,
            "aggregate_type": self.aggregate_type,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AggregateVersion":
        """
        Create an AggregateVersion instance from a dictionary.

        Args:
            data: Dictionary containing aggregate version data

        Returns:
            AggregateVersion instance
        """
        timestamp = None
        if "timestamp" in data:
            timestamp = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))

        return cls(
            aggregate_id=data["aggregate_id"],
            version=data["version"],
            aggregate_type=data["aggregate_type"],
            data=data.get("data", {}),
            timestamp=timestamp,
        )

    def __eq__(self, other: object) -> bool:
        """
        Check equality based on aggregate_id and version.
        """
        if not isinstance(other, AggregateVersion):
            return False

        return self.aggregate_id == other.aggregate_id and self.version == other.version

    def __hash__(self) -> int:
        """
        Hash based on aggregate_id and version.
        """
        return hash((self.aggregate_id, self.version))

    def __repr__(self) -> str:
        """
        String representation of the aggregate version.
        """
        return f"AggregateVersion(id={self.aggregate_id}, version={self.version}, type={self.aggregate_type})"
