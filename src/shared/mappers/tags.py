"""Parameterized mapper for Tags - works with both Sonarr and Radarr."""

from typing import Any, Generic, TypeVar

from src.shared.mappers.base import ResourceMapper

# Generic type for the API model (TagResource from either Sonarr or Radarr)
TTagModel = TypeVar("TTagModel")


class TagMapper(ResourceMapper[TTagModel, str], Generic[TTagModel]):
    """
    Maps tag names to API models.
    
    Parameterized by API model type to support both Sonarr and Radarr.
    """

    def __init__(self, model_class: type[TTagModel]):
        """
        Initialize the mapper with a specific API model class.
        
        Args:
            model_class: The TagResource class (from sonarr_api or radarr_api)
        """
        self.model_class = model_class

    def to_api_model(self, yaml_def: str, **context) -> TTagModel:
        """
        Convert tag name to API model.
        
        Args:
            yaml_def: Tag name (string)
        """
        return self.model_class(label=yaml_def)

    def from_api_model(self, api_model: TTagModel) -> dict[str, Any]:
        """Convert API model to dict for comparison."""
        return {
            "id": api_model.id,
            "label": api_model.label,
        }

    def get_match_key(self, item: dict[str, Any] | TTagModel) -> str:
        """Get the label field for matching."""
        if isinstance(item, dict):
            return item["label"]
        return item.label
