"""Shared Pydantic schemas for resources common across *arr applications."""

from typing import Any, Optional

from pydantic import BaseModel, Field


# ============================================================================
# Custom Formats
# ============================================================================


class CustomFormatSpecificationDef(BaseModel):
    """Definition for a custom format specification (condition)."""

    name: str
    implementation: str
    negate: bool = False
    required: bool = False
    fields: dict[str, Any] = Field(default_factory=dict)


class CustomFormatDef(BaseModel):
    """Definition for a custom format."""

    name: str
    include_custom_format_when_renaming: bool = False
    specifications: list[CustomFormatSpecificationDef] = Field(default_factory=list)


class CustomFormatsConfig(BaseModel):
    """Custom formats section configuration."""

    delete_unmanaged: bool = False
    definitions: list[CustomFormatDef] = Field(default_factory=list)


# ============================================================================
# Quality Profiles
# ============================================================================


class QualityProfileDef(BaseModel):
    """Definition for a quality profile."""

    name: str
    upgrade_allowed: bool = True
    cutoff: str  # Quality name (e.g., "Bluray-1080p")
    items: list[dict[str, Any]]  # Quality items with allowed/quality structure
    min_format_score: int = 0
    cutoff_format_score: int = 0
    min_upgrade_format_score: int = 1
    format_scores: dict[str, int] = Field(
        default_factory=dict
    )  # Custom format name -> score


class QualityProfilesConfig(BaseModel):
    """Quality profiles section configuration."""

    delete_unmanaged: bool = False
    definitions: list[QualityProfileDef] = Field(default_factory=list)


# ============================================================================
# Quality Definitions
# ============================================================================


class QualityDefinitionDef(BaseModel):
    """Definition for a quality definition."""

    title: str  # Quality name (e.g., "HDTV-720p")
    min_size: Optional[float] = None  # GB
    max_size: Optional[float] = None  # GB
    preferred_size: Optional[float] = None  # GB


class QualityDefinitionsConfig(BaseModel):
    """Quality definitions section configuration."""

    definitions: list[QualityDefinitionDef] = Field(default_factory=list)


# ============================================================================
# Tags
# ============================================================================


class TagsConfig(BaseModel):
    """Tags section configuration."""

    delete_unmanaged: bool = False
    definitions: list[str] = Field(default_factory=list)  # Simple list of tag names


# ============================================================================
# Delay Profiles
# ============================================================================


class DelayProfileDef(BaseModel):
    """Definition for a delay profile."""

    preferred_protocol: str = "usenet"  # "usenet", "torrent", or "both"
    usenet_delay: int = 0  # Minutes
    torrent_delay: int = 0  # Minutes
    bypass_if_highest_quality: bool = True
    tags: list[str] = Field(default_factory=list)  # Tag names
    order: Optional[int] = None


class DelayProfilesConfig(BaseModel):
    """Delay profiles section configuration."""

    delete_unmanaged: bool = False
    definitions: list[DelayProfileDef] = Field(default_factory=list)


# ============================================================================
# Indexers
# ============================================================================


class IndexerDef(BaseModel):
    """Definition for an indexer."""

    name: str
    implementation: str  # e.g., "Newznab", "Torznab"
    enable_rss: bool = True
    enable_automatic_search: bool = True
    enable_interactive_search: bool = True
    priority: int = 25
    download_client_id: Optional[int] = None
    tags: list[str] = Field(default_factory=list)
    fields: dict[str, Any] = Field(default_factory=dict)  # Implementation-specific fields


class IndexersConfig(BaseModel):
    """Indexers section configuration."""

    delete_unmanaged: bool = False
    definitions: list[IndexerDef] = Field(default_factory=list)


# ============================================================================
# Download Clients
# ============================================================================


class DownloadClientDef(BaseModel):
    """Definition for a download client."""

    name: str
    implementation: str  # e.g., "Sabnzbd", "QBittorrent"
    enable: bool = True
    priority: int = 1
    remove_completed_downloads: bool = True
    remove_failed_downloads: bool = True
    tags: list[str] = Field(default_factory=list)
    fields: dict[str, Any] = Field(default_factory=dict)  # Implementation-specific fields


class DownloadClientsConfig(BaseModel):
    """Download clients section configuration."""

    delete_unmanaged: bool = False
    definitions: list[DownloadClientDef] = Field(default_factory=list)
