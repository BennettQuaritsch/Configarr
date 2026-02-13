"""Mapper for Indexers."""

from typing import Any

from sonarr_api.models.indexer_resource import IndexerResource

from src.core.config_schema import IndexerDef
from src.mapping.base import ResourceMapper


class IndexerMapper(ResourceMapper[IndexerResource, IndexerDef]):
    """Maps indexer definitions to API models."""

    def to_api_model(self, yaml_def: IndexerDef, **context) -> IndexerResource:
        """
        Convert YAML indexer definition to API model.

        Context should include:
        - tag_map: dict[str, int] - Maps tag names to IDs
        """
        tag_map = context.get("tag_map", {})

        # Convert tag names to IDs
        tag_ids = [tag_map[tag_name] for tag_name in yaml_def.tags if tag_name in tag_map]

        return IndexerResource(
            name=yaml_def.name,
            implementation=yaml_def.implementation,
            enable_rss=yaml_def.enable_rss,
            enable_automatic_search=yaml_def.enable_automatic_search,
            enable_interactive_search=yaml_def.enable_interactive_search,
            priority=yaml_def.priority,
            download_client_id=yaml_def.download_client_id,
            tags=tag_ids,
            fields=yaml_def.fields,
        )

    def from_api_model(self, api_model: IndexerResource) -> dict[str, Any]:
        """Convert API model to dict for comparison."""
        return {
            "id": api_model.id,
            "name": api_model.name,
            "implementation": api_model.implementation,
            "enable_rss": api_model.enable_rss,
            "enable_automatic_search": api_model.enable_automatic_search,
            "enable_interactive_search": api_model.enable_interactive_search,
            "priority": api_model.priority,
            "download_client_id": api_model.download_client_id,
            "tags": api_model.tags or [],
            "fields": api_model.fields,
        }

    def get_match_key(self, item: dict[str, Any] | IndexerResource) -> str:
        """Get the name field for matching."""
        if isinstance(item, dict):
            return item["name"]
        return item.name
