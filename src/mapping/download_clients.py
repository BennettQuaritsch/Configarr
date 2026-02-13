"""Mapper for Download Clients."""

from typing import Any

from sonarr_api.models.download_client_resource import DownloadClientResource

from src.core.config_schema import DownloadClientDef
from src.mapping.base import ResourceMapper


class DownloadClientMapper(ResourceMapper[DownloadClientResource, DownloadClientDef]):
    """Maps download client definitions to API models."""

    def to_api_model(self, yaml_def: DownloadClientDef, **context) -> DownloadClientResource:
        """
        Convert YAML download client definition to API model.

        Context should include:
        - tag_map: dict[str, int] - Maps tag names to IDs
        """
        tag_map = context.get("tag_map", {})

        # Convert tag names to IDs
        tag_ids = [tag_map[tag_name] for tag_name in yaml_def.tags if tag_name in tag_map]

        return DownloadClientResource(
            name=yaml_def.name,
            implementation=yaml_def.implementation,
            enable=yaml_def.enable,
            priority=yaml_def.priority,
            remove_completed_downloads=yaml_def.remove_completed_downloads,
            remove_failed_downloads=yaml_def.remove_failed_downloads,
            tags=tag_ids,
            fields=yaml_def.fields,
        )

    def from_api_model(self, api_model: DownloadClientResource) -> dict[str, Any]:
        """Convert API model to dict for comparison."""
        return {
            "id": api_model.id,
            "name": api_model.name,
            "implementation": api_model.implementation,
            "enable": api_model.enable,
            "priority": api_model.priority,
            "remove_completed_downloads": api_model.remove_completed_downloads,
            "remove_failed_downloads": api_model.remove_failed_downloads,
            "tags": api_model.tags or [],
            "fields": api_model.fields,
        }

    def get_match_key(self, item: dict[str, Any] | DownloadClientResource) -> str:
        """Get the name field for matching."""
        if isinstance(item, dict):
            return item["name"]
        return item.name
