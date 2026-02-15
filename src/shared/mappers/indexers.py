"""Parameterized mapper for Indexers - works with both Sonarr and Radarr."""

from typing import Any, Generic, TypeVar

from src.shared.mappers.base import ResourceMapper
from src.shared.schemas import IndexerDef

# Generic type for API model
TIndexerModel = TypeVar("TIndexerModel")


class IndexerMapper(ResourceMapper[TIndexerModel, IndexerDef], Generic[TIndexerModel]):
    """
    Maps indexer definitions to API models.
    
    Parameterized by API model type to support both Sonarr and Radarr.
    """

    def __init__(self, model_class: type[TIndexerModel]):
        """
        Initialize with specific API model class.
        
        Args:
            model_class: IndexerResource class
        """
        self.model_class = model_class

    def to_api_model(self, yaml_def: IndexerDef, **context) -> TIndexerModel:
        """
        Convert YAML indexer definition to API model.
        
        Context should include:
        - tag_map: dict[str, int] - Maps tag names to IDs
        """
        tag_map = context.get("tag_map", {})

        # Convert tag names to IDs
        tag_ids = [tag_map[tag_name] for tag_name in yaml_def.tags if tag_name in tag_map]

        return self.model_class(
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

    def from_api_model(self, api_model: TIndexerModel) -> dict[str, Any]:
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

    def get_match_key(self, item: dict[str, Any] | TIndexerModel) -> str:
        """Get the name field for matching."""
        if isinstance(item, dict):
            return item["name"]
        return item.name
