"""Sonarr-specific Pydantic schema models."""

from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.shared.schemas import (
    CustomFormatsConfig,
    DelayProfilesConfig,
    DownloadClientsConfig,
    IndexersConfig,
    QualityDefinitionsConfig,
    QualityProfilesConfig,
    TagsConfig,
)


class SonarrNamingConfig(BaseModel):
    """Naming configuration for Sonarr (singleton resource)."""

    rename_episodes: bool = True
    replace_illegal_characters: bool = True
    standard_episode_format: str
    daily_episode_format: str = "{Series TitleYear} - {Air-Date} - {Episode CleanTitle} [{Preferred Words }{Quality Full}]{[MediaInfo VideoDynamicRangeType]}{[Mediainfo AudioCodec}{ Mediainfo AudioChannels]}{MediaInfo AudioLanguages}{-Release Group}"
    anime_episode_format: str = "{Series TitleYear} - S{season:00}E{episode:00} - {absolute:000} - {Episode CleanTitle} [{Preferred Words }{Quality Full}]{[MediaInfo VideoDynamicRangeType]}[{MediaInfo VideoBitDepth}bit]{[MediaInfo VideoCodec]}[{Mediainfo AudioCodec} { Mediainfo AudioChannels}]{MediaInfo AudioLanguages}{-Release Group}"
    series_folder_format: str = "{Series TitleYear} [imdbid-{ImdbId}]"
    season_folder_format: str = "Season {season:00}"
    specials_folder_format: str = "Specials"
    multi_episode_style: int = 0  # 0=Extend, 1=Duplicate, 2=Repeat, 3=Scene, 4=Range, 5=Prefixed Range


class SonarrMediaManagementConfig(BaseModel):
    """Media management configuration for Sonarr (singleton resource)."""

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
    naming: Optional[SonarrNamingConfig] = None
    media_management: Optional[SonarrMediaManagementConfig] = None

    @field_validator("base_url", "api_key")
    @classmethod
    def validate_credentials(cls, v: Optional[str], info) -> Optional[str]:
        """Validate that credentials are provided (either inline or via env vars)."""
        # The actual interpolation happens in yaml_loader
        return v
