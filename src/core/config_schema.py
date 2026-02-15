"""Root configuration schema for Configarr."""

from pydantic import BaseModel, Field, field_validator

from src.plugins.sonarr.schema import SonarrInstanceConfig


# ============================================================================
# Root Configuration
# ============================================================================
#
# Shared resource schemas have been moved to src/shared/schemas.py
# Plugin-specific schemas (e.g., SonarrInstanceConfig) are now in plugin directories
# ============================================================================


class ConfigarrConfig(BaseModel):
    """Root configuration model for Configarr."""

    sonarr: list[SonarrInstanceConfig] = Field(
        default_factory=list, description="List of Sonarr instances to manage"
    )
    # Future plugins will add their keys here (radarr, prowlarr, etc.)

    @field_validator("sonarr")
    @classmethod
    def validate_unique_sonarr_names(cls, instances: list[SonarrInstanceConfig]) -> list[SonarrInstanceConfig]:
        """Ensure all Sonarr instance names are unique."""
        names = [inst.name for inst in instances]
        if len(names) != len(set(names)):
            duplicates = [name for name in names if names.count(name) > 1]
            raise ValueError(f"Duplicate Sonarr instance names found: {set(duplicates)}")
        return instances
