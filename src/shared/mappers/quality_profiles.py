"""Parameterized mapper for Quality Profiles - works with both Sonarr and Radarr."""

from typing import Any, Generic, TypeVar

from src.shared.mappers.base import ResourceMapper
from src.shared.schemas import QualityProfileDef

# Generic types for API models
TQualityProfileModel = TypeVar("TQualityProfileModel")
TProfileFormatItemModel = TypeVar("TProfileFormatItemModel")


class QualityProfileMapper(
    ResourceMapper[TQualityProfileModel, QualityProfileDef],
    Generic[TQualityProfileModel, TProfileFormatItemModel],
):
    """
    Maps quality profile definitions to API models.
    
    Parameterized by API model types to support both Sonarr and Radarr.
    """

    def __init__(
        self,
        profile_model_class: type[TQualityProfileModel],
        format_item_model_class: type[TProfileFormatItemModel],
    ):
        """
        Initialize with specific API model classes.
        
        Args:
            profile_model_class: QualityProfileResource class
            format_item_model_class: ProfileFormatItemResource class
        """
        self.profile_model_class = profile_model_class
        self.format_item_model_class = format_item_model_class

    def to_api_model(self, yaml_def: QualityProfileDef, **context) -> TQualityProfileModel:
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
            self.format_item_model_class(format=custom_format_map.get(cf_name), score=score)
            for cf_name, score in yaml_def.format_scores.items()
            if cf_name in custom_format_map
        ]

        return self.profile_model_class(
            name=yaml_def.name,
            upgrade_allowed=yaml_def.upgrade_allowed,
            cutoff=cutoff_id,
            items=yaml_def.items,
            min_format_score=yaml_def.min_format_score,
            cutoff_format_score=yaml_def.cutoff_format_score,
            min_upgrade_format_score=yaml_def.min_upgrade_format_score,
            format_items=format_items,
        )

    def from_api_model(self, api_model: TQualityProfileModel) -> dict[str, Any]:
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

    def get_match_key(self, item: dict[str, Any] | TQualityProfileModel) -> str:
        """Get the name field for matching."""
        if isinstance(item, dict):
            return item["name"]
        return item.name
