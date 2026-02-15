"""Mapper for Sonarr Media Management Configuration."""

from typing import Any

from sonarr_api.models.media_management_config_resource import MediaManagementConfigResource

from src.plugins.sonarr.schema import SonarrMediaManagementConfig
from src.shared.mappers.base import ResourceMapper


class MediaManagementConfigMapper(
    ResourceMapper[MediaManagementConfigResource, SonarrMediaManagementConfig]
):
    """Maps media management configuration to API models."""

    def to_api_model(
        self, yaml_def: SonarrMediaManagementConfig, **context
    ) -> MediaManagementConfigResource:
        """
        Convert YAML media management config to API model.

        Context should include:
        - existing_config: MediaManagementConfigResource - The current config from server (has ID)
        """
        existing = context.get("existing_config")
        config_id = existing.id if existing else None

        return MediaManagementConfigResource(
            id=config_id,
            auto_unmonitor_previously_downloaded_episodes=yaml_def.auto_unmonitor_previously_downloaded_episodes,
            recycle_bin=yaml_def.recycle_bin,
            recycle_bin_cleanup_days=yaml_def.recycle_bin_cleanup_days,
            download_propers_and_repacks=yaml_def.download_propers_and_repacks,
            create_empty_series_folders=yaml_def.create_empty_series_folders,
            delete_empty_folders=yaml_def.delete_empty_folders,
            file_date=yaml_def.file_date,
            rescan_after_refresh=yaml_def.rescan_after_refresh,
            set_permissions_linux=yaml_def.set_permissions_linux,
            chmod_folder=yaml_def.chmod_folder,
            chown_group=yaml_def.chown_group,
            skip_free_space_check_when_importing=yaml_def.skip_free_space_check_when_importing,
            minimum_free_space_when_importing=yaml_def.minimum_free_space_when_importing,
            copy_using_hardlinks=yaml_def.copy_using_hardlinks,
            import_extra_files=yaml_def.import_extra_files,
            extra_file_extensions=yaml_def.extra_file_extensions,
        )

    def from_api_model(self, api_model: MediaManagementConfigResource) -> dict[str, Any]:
        """Convert API model to dict for comparison."""
        return {
            "id": api_model.id,
            "auto_unmonitor_previously_downloaded_episodes": api_model.auto_unmonitor_previously_downloaded_episodes,
            "recycle_bin": api_model.recycle_bin,
            "recycle_bin_cleanup_days": api_model.recycle_bin_cleanup_days,
            "download_propers_and_repacks": api_model.download_propers_and_repacks,
            "create_empty_series_folders": api_model.create_empty_series_folders,
            "delete_empty_folders": api_model.delete_empty_folders,
            "file_date": api_model.file_date,
            "rescan_after_refresh": api_model.rescan_after_refresh,
            "set_permissions_linux": api_model.set_permissions_linux,
            "chmod_folder": api_model.chmod_folder,
            "chown_group": api_model.chown_group,
            "skip_free_space_check_when_importing": api_model.skip_free_space_check_when_importing,
            "minimum_free_space_when_importing": api_model.minimum_free_space_when_importing,
            "copy_using_hardlinks": api_model.copy_using_hardlinks,
            "import_extra_files": api_model.import_extra_files,
            "extra_file_extensions": api_model.extra_file_extensions,
        }

    def get_match_key(self, item: dict[str, Any] | MediaManagementConfigResource) -> str:
        """Media management config is a singleton, so always return a constant key."""
        return "media_management_config"
