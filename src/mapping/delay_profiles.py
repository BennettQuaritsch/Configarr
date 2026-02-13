"""Mapper for Delay Profiles."""

from typing import Any

from sonarr_api.models.delay_profile_resource import DelayProfileResource

from src.core.config_schema import DelayProfileDef
from src.mapping.base import ResourceMapper


class DelayProfileMapper(ResourceMapper[DelayProfileResource, DelayProfileDef]):
    """Maps delay profile definitions to API models."""

    def to_api_model(self, yaml_def: DelayProfileDef, **context) -> DelayProfileResource:
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
            "both": "usenetPrefer",  # or "torrentPrefer" - default to usenet
        }
        preferred_protocol = protocol_map.get(
            yaml_def.preferred_protocol.lower(), "usenetPrefer"
        )

        return DelayProfileResource(
            preferred_protocol=preferred_protocol,
            usenet_delay=yaml_def.usenet_delay,
            torrent_delay=yaml_def.torrent_delay,
            bypass_if_highest_quality=yaml_def.bypass_if_highest_quality,
            tags=tag_ids,
            order=yaml_def.order,
        )

    def from_api_model(self, api_model: DelayProfileResource) -> dict[str, Any]:
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

    def get_match_key(self, item: dict[str, Any] | DelayProfileResource) -> str:
        """
        Delay profiles don't have names, so we match by tag combination.

        Returns a string representation of sorted tag IDs.
        """
        if isinstance(item, dict):
            tags = sorted(item.get("tags", []))
        else:
            tags = sorted(item.tags or [])
        return ",".join(map(str, tags))
