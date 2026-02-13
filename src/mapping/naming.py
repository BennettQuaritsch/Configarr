"""Mapper for Naming Configuration."""

from typing import Any

from sonarr_api.models.naming_config_resource import NamingConfigResource

from src.core.config_schema import NamingConfig
from src.mapping.base import ResourceMapper


class NamingConfigMapper(ResourceMapper[NamingConfigResource, NamingConfig]):
    """Maps naming configuration to API models."""

    def to_api_model(self, yaml_def: NamingConfig, **context) -> NamingConfigResource:
        """
        Convert YAML naming config to API model.

        Context should include:
        - existing_config: NamingConfigResource - The current config from server (has ID)
        """
        existing = context.get("existing_config")
        config_id = existing.id if existing else None

        return NamingConfigResource(
            id=config_id,
            rename_episodes=yaml_def.rename_episodes,
            replace_illegal_characters=yaml_def.replace_illegal_characters,
            standard_episode_format=yaml_def.standard_episode_format,
            daily_episode_format=yaml_def.daily_episode_format,
            anime_episode_format=yaml_def.anime_episode_format,
            series_folder_format=yaml_def.series_folder_format,
            season_folder_format=yaml_def.season_folder_format,
            specials_folder_format=yaml_def.specials_folder_format,
            multi_episode_style=yaml_def.multi_episode_style,
        )

    def from_api_model(self, api_model: NamingConfigResource) -> dict[str, Any]:
        """Convert API model to dict for comparison."""
        return {
            "id": api_model.id,
            "rename_episodes": api_model.rename_episodes,
            "replace_illegal_characters": api_model.replace_illegal_characters,
            "standard_episode_format": api_model.standard_episode_format,
            "daily_episode_format": api_model.daily_episode_format,
            "anime_episode_format": api_model.anime_episode_format,
            "series_folder_format": api_model.series_folder_format,
            "season_folder_format": api_model.season_folder_format,
            "specials_folder_format": api_model.specials_folder_format,
            "multi_episode_style": api_model.multi_episode_style,
        }

    def get_match_key(self, item: dict[str, Any] | NamingConfigResource) -> str:
        """Naming config is a singleton, so always return a constant key."""
        return "naming_config"
