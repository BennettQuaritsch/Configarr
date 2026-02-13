"""Diff utilities for comparing desired and current state."""

from dataclasses import dataclass
from typing import Any, Generic, TypeVar

T = TypeVar("T")


@dataclass
class ChangeSet(Generic[T]):
    """
    Represents the changes needed to reconcile current and desired state.

    Attributes:
        to_create: Items that need to be created
        to_update: Tuples of (current_item, desired_item) that need updates
        to_delete: Items that need to be deleted
    """

    to_create: list[T]
    to_update: list[tuple[dict[str, Any], T]]  # (current, desired)
    to_delete: list[dict[str, Any]]

    def __bool__(self) -> bool:
        """Return True if there are any changes."""
        return bool(self.to_create or self.to_update or self.to_delete)

    def summary(self) -> str:
        """Return a human-readable summary of the changeset."""
        parts = []
        if self.to_create:
            parts.append(f"{len(self.to_create)} to create")
        if self.to_update:
            parts.append(f"{len(self.to_update)} to update")
        if self.to_delete:
            parts.append(f"{len(self.to_delete)} to delete")

        if not parts:
            return "no changes"

        return ", ".join(parts)


def compute_diff(
    current: list[dict[str, Any]],
    desired: list[Any],
    match_key_fn: callable,
    needs_update_fn: callable,
    delete_unmanaged: bool = False,
) -> ChangeSet:
    """
    Compare current server state with desired YAML state and compute changes.

    Args:
        current: List of current resources from server (as dicts)
        desired: List of desired resources from YAML
        match_key_fn: Function to extract match key from an item
        needs_update_fn: Function(current_dict, desired_dict) -> bool
        delete_unmanaged: Whether to delete items not in desired state

    Returns:
        ChangeSet with items to create, update, and delete
    """
    # Build lookup maps by match key
    current_map = {match_key_fn(item): item for item in current}
    desired_map = {match_key_fn(item): item for item in desired}

    to_create = []
    to_update = []
    to_delete = []

    # Find items to create or update
    for key, desired_item in desired_map.items():
        if key not in current_map:
            # Doesn't exist on server -> create
            to_create.append(desired_item)
        else:
            # Exists on server -> check if update needed
            current_item = current_map[key]
            if needs_update_fn(current_item, desired_item):
                to_update.append((current_item, desired_item))

    # Find items to delete (if enabled)
    if delete_unmanaged:
        for key, current_item in current_map.items():
            if key not in desired_map:
                to_delete.append(current_item)

    return ChangeSet(to_create=to_create, to_update=to_update, to_delete=to_delete)
