"""Pydantic models defining the YAML configuration schema for ADM."""

from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


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


# ============================================================================
# Naming Configuration
# ============================================================================


class NamingConfig(BaseModel):
    """Naming configuration (singleton resource)."""

    rename_episodes: bool = True
    replace_illegal_characters: bool = True
    standard_episode_format: str
    daily_episode_format: str = "{Series TitleYear} - {Air-Date} - {Episode CleanTitle} [{Preferred Words }{Quality Full}]{[MediaInfo VideoDynamicRangeType]}{[Mediainfo AudioCodec}{ Mediainfo AudioChannels]}{MediaInfo AudioLanguages}{-Release Group}"
    anime_episode_format: str = "{Series TitleYear} - S{season:00}E{episode:00} - {absolute:000} - {Episode CleanTitle} [{Preferred Words }{Quality Full}]{[MediaInfo VideoDynamicRangeType]}[{MediaInfo VideoBitDepth}bit]{[MediaInfo VideoCodec]}[{Mediainfo AudioCodec} { Mediainfo AudioChannels}]{MediaInfo AudioLanguages}{-Release Group}"
    series_folder_format: str = "{Series TitleYear} [imdbid-{ImdbId}]"
    season_folder_format: str = "Season {season:00}"
    specials_folder_format: str = "Specials"
    multi_episode_style: int = 0  # 0=Extend, 1=Duplicate, 2=Repeat, 3=Scene, 4=Range, 5=Prefixed Range


# ============================================================================
# Media Management Configuration
# ============================================================================


class MediaManagementConfig(BaseModel):
    """Media management configuration (singleton resource)."""

    auto_unmonitor_previously_downloaded_episodes: bool = False
    recycle_bin: Optional[str] = None  # Path to recycle bin
    recycle_bin_cleanup_days: int = 7
    download_propers_and_repacks: str = "preferAndUpgrade"  # doNotUpgrade/preferAndUpgrade
    create_empty_series_folders: bool = False
    delete_empty_folders: bool = False
    file_date: str = "none"  # none/cinemas/localAirDate/utcAirDate
    rescan_after_refresh: str = "always"  # always/afterManual/never
    set_permissions_linux: bool = False
    chmod_folder: str = "755"
    chown_group: Optional[str] = None
    skip_free_space_check_when_importing: bool = False
    minimum_free_space_when_importing: int = 100  # MB
    copy_using_hardlinks: bool = True
    import_extra_files: bool = False
    extra_file_extensions: str = "srt,nfo"


# ============================================================================
# Sonarr Instance Configuration
# ============================================================================


class SonarrInstanceConfig(BaseModel):
    """Configuration for a single Sonarr instance."""

    name: str = Field(..., description="Unique instance identifier")
    base_url: Optional[str] = Field(
        None, description="Base URL (can use ${ENV_VAR} or load from env)"
    )
    api_key: Optional[str] = Field(
        None, description="API key (can use ${ENV_VAR} or load from env)"
    )

    # Resource sections
    custom_formats: Optional[CustomFormatsConfig] = None
    quality_profiles: Optional[QualityProfilesConfig] = None
    quality_definitions: Optional[QualityDefinitionsConfig] = None
    tags: Optional[TagsConfig] = None
    delay_profiles: Optional[DelayProfilesConfig] = None
    indexers: Optional[IndexersConfig] = None
    download_clients: Optional[DownloadClientsConfig] = None
    naming: Optional[NamingConfig] = None
    media_management: Optional[MediaManagementConfig] = None

    @field_validator("base_url", "api_key")
    @classmethod
    def validate_credentials(cls, v: Optional[str], info) -> Optional[str]:
        """Validate that credentials are provided (either inline or via env vars)."""
        field_name = info.field_name
        # If value is provided (even if it's an env var reference), that's OK
        # The actual interpolation happens in yaml_loader
        return v


# ============================================================================
# Root Configuration
# ============================================================================


class ADMConfig(BaseModel):
    """Root configuration model for ADM."""

    sonarr: list[SonarrInstanceConfig] = Field(
        default_factory=list, description="List of Sonarr instances to manage"
    )
    # Future: radarr, prowlarr, etc.

    @field_validator("sonarr")
    @classmethod
    def validate_unique_names(cls, instances: list[SonarrInstanceConfig]) -> list[SonarrInstanceConfig]:
        """Ensure all instance names are unique."""
        names = [inst.name for inst in instances]
        if len(names) != len(set(names)):
            duplicates = [name for name in names if names.count(name) > 1]
            raise ValueError(f"Duplicate instance names found: {set(duplicates)}")
        return instances
