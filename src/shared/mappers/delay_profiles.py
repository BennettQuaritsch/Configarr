"""Parameterized mapper for Delay Profiles - works with both Sonarr and Radarr."""

from typing import Any, Generic, TypeVar

from src.shared.mappers.base import ResourceMapper
from src.shared.schemas import DelayProfileDef

# Generic type for API model
TDelayProfileModel = TypeVar("TDelayProfileModel")


class DelayProfileMapper(
    ResourceMapper[TDelayProfileModel, DelayProfileDef], Generic[TDelayProfileModel]
):
    """
    Maps delay profile definitions to API models.
    
    Parameterized by API model type to support both Sonarr and Radarr.
    """

    def __init__(self, model_class: type[TDelayProfileModel]):
        """
        Initialize with specific API model class.
        
        Args:
            model_class: DelayProfileResource class
        """
        self.model_class = model_class

    def to_api_model(self, yaml_def: DelayProfileDef, **context) -> TDelayProfileModel:
        """
        Convert YAML delay profile definition to API model.
        
        Context should include:
        - tag_map: dict[str, int] - Maps tag names to IDs
        """
        tag_map = context.get("tag_map", {})

        # Convert tag names to IDs
        tag_ids = [tag_map[tag_name] for tag_name in yaml_def.tags if tag_name in tag_map]

        # Map protocol string to enum value
        protocol_map = {
            "usenet": "usenet",
            "torrent": "torrent",
            "both": "usenetPrefer",
        }
        preferred_protocol = protocol_map.get(
            yaml_def.preferred_protocol.lower(), "usenetPrefer"
        )

        return self.model_class(
            preferred_protocol=preferred_protocol,
            usenet_delay=yaml_def.usenet_delay,
            torrent_delay=yaml_def.torrent_delay,
            bypass_if_highest_quality=yaml_def.bypass_if_highest_quality,
            tags=tag_ids,
            order=yaml_def.order,
        )

    def from_api_model(self, api_model: TDelayProfileModel) -> dict[str, Any]:
        """Convert API model to dict for comparison."""
        return {
            "id": api_model.id,
            "preferred_protocol": api_model.preferred_protocol,
            "usenet_delay": api_model.usenet_delay,
            "torrent_delay": api_model.torrent_delay,
            "bypass_if_highest_quality": api_model.bypass_if_highest_quality,
            "tags": api_model.tags or [],
            "order": api_model.order,
        }

    def get_match_key(self, item: dict[str, Any] | TDelayProfileModel) -> str:
        """
        Delay profiles don't have names, so we match by tag combination.
        
        Returns a string representation of sorted tag IDs.
        """
        if isinstance(item, dict):
            tags = sorted(item.get("tags", []))
        else:
            tags = sorted(item.tags or [])
        return ",".join(map(str, tags))
