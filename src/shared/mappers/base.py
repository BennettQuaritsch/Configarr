"""Base class for resource mappers."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

# Type variables for API models and YAML definitions
TApiModel = TypeVar("TApiModel")
TYamlDef = TypeVar("TYamlDef")


class ResourceMapper(ABC, Generic[TApiModel, TYamlDef]):
    """
    Abstract base class for mapping between YAML config and API models.

    Each resource type (custom formats, quality profiles, etc.) should
    have its own mapper that extends this class.
    """

    @abstractmethod
    def to_api_model(self, yaml_def: TYamlDef, **context) -> TApiModel:
        """
        Convert a YAML definition to an API model object.

        Args:
            yaml_def: YAML definition object (from config_schema.py)
            **context: Additional context needed for mapping (e.g., tag ID lookups)

        Returns:
            API model object ready to send to Sonarr
        """
        pass

    @abstractmethod
    def from_api_model(self, api_model: TApiModel) -> dict[str, Any]:
        """
        Convert an API model to a dictionary representation.

        This is used for comparison and logging purposes.

        Args:
            api_model: API model object from Sonarr

        Returns:
            Dictionary representation
        """
        pass

    @abstractmethod
    def get_match_key(self, item: dict[str, Any] | TApiModel) -> str:
        """
        Get the unique identifier for matching resources.

        This is typically the 'name' field, but can vary by resource type.

        Args:
            item: Either a dict or an API model object

        Returns:
            Unique identifier string
        """
        pass

    def needs_update(
        self, current: dict[str, Any], desired: dict[str, Any], ignore_fields: list[str] = None
    ) -> bool:
        """
        Compare current and desired state to determine if an update is needed.

        Args:
            current: Current state (from server)
            desired: Desired state (from YAML)
            ignore_fields: Fields to ignore in comparison (e.g., 'id', 'updated_at')

        Returns:
            True if update is needed
        """
        ignore_fields = ignore_fields or ["id"]

        for key, desired_value in desired.items():
            if key in ignore_fields:
                continue

            current_value = current.get(key)

            # Handle nested comparisons
            if isinstance(desired_value, dict) and isinstance(current_value, dict):
                if self._dict_differs(current_value, desired_value, ignore_fields):
                    return True
            elif isinstance(desired_value, list) and isinstance(current_value, list):
                if self._list_differs(current_value, desired_value):
                    return True
            elif current_value != desired_value:
                return True

        return False

    def _dict_differs(
        self, current: dict, desired: dict, ignore_fields: list[str] = None
    ) -> bool:
        """Check if two dicts differ."""
        ignore_fields = ignore_fields or []
        for key, val in desired.items():
            if key in ignore_fields:
                continue
            if key not in current or current[key] != val:
                return True
        return False

    def _list_differs(self, current: list, desired: list) -> bool:
        """Check if two lists differ (order-independent for lists of dicts)."""
        if len(current) != len(desired):
            return True

        # For simple lists (strings, numbers)
        if current and not isinstance(current[0], (dict, list)):
            return sorted(current) != sorted(desired)

        # For lists of dicts, compare as sets
        # This is a simplified comparison; override if needed
        return current != desired
