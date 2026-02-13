"""Mapper for Custom Formats."""

from typing import Any

from sonarr_api.models.custom_format_resource import CustomFormatResource
from sonarr_api.models.custom_format_specification_schema import (
    CustomFormatSpecificationSchema,
)

from src.core.config_schema import CustomFormatDef, CustomFormatSpecificationDef
from src.mapping.base import ResourceMapper


class CustomFormatMapper(ResourceMapper[CustomFormatResource, CustomFormatDef]):
    """Maps custom format definitions to API models."""

    def to_api_model(self, yaml_def: CustomFormatDef, **context) -> CustomFormatResource:
        """Convert YAML custom format definition to API model."""
        specifications = [
            CustomFormatSpecificationSchema(
                name=spec.name,
                implementation=spec.implementation,
                negate=spec.negate,
                required=spec.required,
                fields=spec.fields,
            )
            for spec in yaml_def.specifications
        ]

        return CustomFormatResource(
            name=yaml_def.name,
            include_custom_format_when_renaming=yaml_def.include_custom_format_when_renaming,
            specifications=specifications,
        )

    def from_api_model(self, api_model: CustomFormatResource) -> dict[str, Any]:
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

    def get_match_key(self, item: dict[str, Any] | CustomFormatResource) -> str:
        """Get the name field for matching."""
        if isinstance(item, dict):
            return item["name"]
        return item.name
