"""Mapper for Quality Profiles."""

from typing import Any

from sonarr_api.models.profile_format_item_resource import ProfileFormatItemResource
from sonarr_api.models.quality_profile_resource import QualityProfileResource

from src.core.config_schema import QualityProfileDef
from src.mapping.base import ResourceMapper


class QualityProfileMapper(ResourceMapper[QualityProfileResource, QualityProfileDef]):
    """Maps quality profile definitions to API models."""

    def to_api_model(self, yaml_def: QualityProfileDef, **context) -> QualityProfileResource:
        """
        Convert YAML quality profile definition to API model.

        Context should include:
        - custom_format_map: dict[str, int] - Maps CF names to IDs
        - cutoff_id: int - Quality ID for cutoff
        """
        custom_format_map = context.get("custom_format_map", {})
        cutoff_id = context.get("cutoff_id")

        # Convert format_scores dict to ProfileFormatItemResource list
        format_items = [
            ProfileFormatItemResource(format=custom_format_map.get(cf_name), score=score)
            for cf_name, score in yaml_def.format_scores.items()
            if cf_name in custom_format_map
        ]

        return QualityProfileResource(
            name=yaml_def.name,
            upgrade_allowed=yaml_def.upgrade_allowed,
            cutoff=cutoff_id,
            items=yaml_def.items,  # Pass through as-is (already in correct format)
            min_format_score=yaml_def.min_format_score,
            cutoff_format_score=yaml_def.cutoff_format_score,
            min_upgrade_format_score=yaml_def.min_upgrade_format_score,
            format_items=format_items,
        )

    def from_api_model(self, api_model: QualityProfileResource) -> dict[str, Any]:
        """Convert API model to dict for comparison."""
        return {
            "id": api_model.id,
            "name": api_model.name,
            "upgrade_allowed": api_model.upgrade_allowed,
            "cutoff": api_model.cutoff,
            "items": api_model.items,
            "min_format_score": api_model.min_format_score,
            "cutoff_format_score": api_model.cutoff_format_score,
            "min_upgrade_format_score": api_model.min_upgrade_format_score,
            "format_items": [
                {"format": item.format, "score": item.score}
                for item in (api_model.format_items or [])
            ],
        }

    def get_match_key(self, item: dict[str, Any] | QualityProfileResource) -> str:
        """Get the name field for matching."""
        if isinstance(item, dict):
            return item["name"]
        return item.name
