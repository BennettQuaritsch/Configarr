"""Parameterized mapper for Custom Formats - works with both Sonarr and Radarr."""

from typing import Any, Generic, TypeVar

from src.shared.mappers.base import ResourceMapper
from src.shared.schemas import CustomFormatDef

# Generic types for API models
TCustomFormatModel = TypeVar("TCustomFormatModel")
TCustomFormatSpecModel = TypeVar("TCustomFormatSpecModel")


class CustomFormatMapper(
    ResourceMapper[TCustomFormatModel, CustomFormatDef],
    Generic[TCustomFormatModel, TCustomFormatSpecModel],
):
    """
    Maps custom format definitions to API models.
    
    Parameterized by API model types to support both Sonarr and Radarr.
    """

    def __init__(
        self,
        format_model_class: type[TCustomFormatModel],
        spec_model_class: type[TCustomFormatSpecModel],
    ):
        """
        Initialize with specific API model classes.
        
        Args:
            format_model_class: CustomFormatResource class
            spec_model_class: CustomFormatSpecificationSchema class
        """
        self.format_model_class = format_model_class
        self.spec_model_class = spec_model_class

    def to_api_model(self, yaml_def: CustomFormatDef, **context) -> TCustomFormatModel:
        """Convert YAML custom format definition to API model."""
        specifications = [
            self.spec_model_class(
                name=spec.name,
                implementation=spec.implementation,
                negate=spec.negate,
                required=spec.required,
                fields=spec.fields,
            )
            for spec in yaml_def.specifications
        ]

        return self.format_model_class(
            name=yaml_def.name,
            include_custom_format_when_renaming=yaml_def.include_custom_format_when_renaming,
            specifications=specifications,
        )

    def from_api_model(self, api_model: TCustomFormatModel) -> dict[str, Any]:
        """Convert API model to dict for comparison."""
        return {
            "id": api_model.id,
            "name": api_model.name,
            "include_custom_format_when_renaming": api_model.include_custom_format_when_renaming,
            "specifications": [
                {
                    "name": spec.name,
                    "implementation": spec.implementation,
                    "negate": spec.negate,
                    "required": spec.required,
                    "fields": spec.fields,
                }
                for spec in (api_model.specifications or [])
            ],
        }

    def get_match_key(self, item: dict[str, Any] | TCustomFormatModel) -> str:
        """Get the name field for matching."""
        if isinstance(item, dict):
            return item["name"]
        return item.name
