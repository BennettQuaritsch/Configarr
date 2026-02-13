"""Mapper for Quality Definitions."""

from typing import Any

from sonarr_api.models.quality_definition_resource import QualityDefinitionResource

from src.core.config_schema import QualityDefinitionDef
from src.mapping.base import ResourceMapper


class QualityDefinitionMapper(ResourceMapper[QualityDefinitionResource, QualityDefinitionDef]):
    """Maps quality definition configurations to API models."""

    def to_api_model(
        self, yaml_def: QualityDefinitionDef, **context
    ) -> QualityDefinitionResource:
        """
        Convert YAML quality definition to API model.

        Context should include:
        - existing_definition: QualityDefinitionResource - The current definition from server
        """
        existing = context.get("existing_definition")
        if not existing:
            raise ValueError(
                f"Quality definition '{yaml_def.title}' requires existing definition from server"
            )

        # Quality definitions are updated in place, not created
        # We preserve the server's ID and quality info, just update sizes
        return QualityDefinitionResource(
            id=existing.id,
            quality=existing.quality,
            title=existing.title,
            weight=existing.weight,
            min_size=yaml_def.min_size,
            max_size=yaml_def.max_size,
            preferred_size=yaml_def.preferred_size,
        )

    def from_api_model(self, api_model: QualityDefinitionResource) -> dict[str, Any]:
        """Convert API model to dict for comparison."""
        return {
            "id": api_model.id,
            "title": api_model.title,
            "min_size": api_model.min_size,
            "max_size": api_model.max_size,
            "preferred_size": api_model.preferred_size,
            "weight": api_model.weight,
        }

    def get_match_key(self, item: dict[str, Any] | QualityDefinitionResource) -> str:
        """Get the title field for matching."""
        if isinstance(item, dict):
            return item["title"]
        return item.title
