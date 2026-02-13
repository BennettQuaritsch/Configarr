"""Mapper for Tags."""

from typing import Any

from sonarr_api.models.tag_resource import TagResource

from src.mapping.base import ResourceMapper


class TagMapper(ResourceMapper[TagResource, str]):
    """Maps tag names to API models."""

    def to_api_model(self, yaml_def: str, **context) -> TagResource:
        """
        Convert tag name to API model.

        Args:
            yaml_def: Tag name (string)
        """
        return TagResource(label=yaml_def)

    def from_api_model(self, api_model: TagResource) -> dict[str, Any]:
        """Convert API model to dict for comparison."""
        return {
            "id": api_model.id,
            "label": api_model.label,
        }

    def get_match_key(self, item: dict[str, Any] | TagResource) -> str:
        """Get the label field for matching."""
        if isinstance(item, dict):
            return item["label"]
        return item.label
