"""Sonarr plugin implementation for Configarr."""

from typing import Any

from pydantic import BaseModel
from sonarr_api.models.custom_format_resource import CustomFormatResource
from sonarr_api.models.custom_format_specification_schema import CustomFormatSpecificationSchema
from sonarr_api.models.delay_profile_resource import DelayProfileResource
from sonarr_api.models.download_client_resource import DownloadClientResource
from sonarr_api.models.indexer_resource import IndexerResource
from sonarr_api.models.profile_format_item_resource import ProfileFormatItemResource
from sonarr_api.models.quality_definition_resource import QualityDefinitionResource
from sonarr_api.models.quality_profile_resource import QualityProfileResource
from sonarr_api.models.tag_resource import TagResource

from src.plugins.base import ArrClient, ArrPlugin, ResourceDefinition
from src.plugins.sonarr.client import SonarrClient
from src.plugins.sonarr.mappers.media_management import MediaManagementConfigMapper
from src.plugins.sonarr.mappers.naming import NamingConfigMapper
from src.plugins.sonarr.schema import SonarrInstanceConfig
from src.shared.mappers.custom_formats import CustomFormatMapper
from src.shared.mappers.delay_profiles import DelayProfileMapper
from src.shared.mappers.download_clients import DownloadClientMapper
from src.shared.mappers.indexers import IndexerMapper
from src.shared.mappers.quality_definitions import QualityDefinitionMapper
from src.shared.mappers.quality_profiles import QualityProfileMapper
from src.shared.mappers.tags import TagMapper


class SonarrPlugin(ArrPlugin):
    """Sonarr implementation of the ArrPlugin interface."""

    @property
    def name(self) -> str:
        return "sonarr"

    @property
    def display_name(self) -> str:
        return "Sonarr"

    @property
    def config_key(self) -> str:
        return "sonarr"

    def get_client(self, base_url: str, api_key: str) -> ArrClient:
        return SonarrClient(base_url=base_url, api_key=api_key)

    def get_instance_schema(self) -> type[BaseModel]:
        return SonarrInstanceConfig

    def get_resource_definitions(
        self, client: SonarrClient, instance_config: SonarrInstanceConfig
    ) -> list[ResourceDefinition]:
        """
        Build ordered list of resources to reconcile for Sonarr.
        
        Resources are ordered by dependency: tags first, then resources that depend on tags, etc.
        """
        definitions = []

        # 1. Tags (no dependencies)
        if instance_config.tags:
            tag_mapper = TagMapper(TagResource)
            definitions.append(
                ResourceDefinition(
                    name="tags",
                    order=1,
                    mapper=tag_mapper,
                    list_fn=lambda: client.tags.api_v3_tag_get(),
                    create_fn=lambda model: client.tags.api_v3_tag_post(tag_resource=model),
                    update_fn=lambda id, model: client.tags.api_v3_tag_id_put(
                        id=id, tag_resource=model
                    ),
                    delete_fn=lambda id: client.tags.api_v3_tag_id_delete(id=id),
                )
            )

        # 2. Custom Formats (no dependencies)
        if instance_config.custom_formats:
            cf_mapper = CustomFormatMapper(CustomFormatResource, CustomFormatSpecificationSchema)
            definitions.append(
                ResourceDefinition(
                    name="custom_formats",
                    order=2,
                    mapper=cf_mapper,
                    list_fn=lambda: client.custom_formats.api_v3_customformat_get(),
                    create_fn=lambda model: client.custom_formats.api_v3_customformat_post(
                        custom_format_resource=model
                    ),
                    update_fn=lambda id, model: client.custom_formats.api_v3_customformat_id_put(
                        id=id, custom_format_resource=model
                    ),
                    delete_fn=lambda id: client.custom_formats.api_v3_customformat_id_delete(id=id),
                )
            )

        # 3. Quality Definitions (no dependencies, but updates only)
        if instance_config.quality_definitions:
            qd_mapper = QualityDefinitionMapper(QualityDefinitionResource)
            definitions.append(
                ResourceDefinition(
                    name="quality_definitions",
                    order=3,
                    mapper=qd_mapper,
                    list_fn=lambda: client.quality_definitions.api_v3_qualitydefinition_get(),
                    create_fn=lambda model: None,  # No create for quality definitions
                    update_fn=lambda id, model: client.quality_definitions.api_v3_qualitydefinition_id_put(
                        id=id, quality_definition_resource=model
                    ),
                    delete_fn=None,  # No delete for quality definitions
                )
            )

        # 4. Quality Profiles (depends on custom formats)
        if instance_config.quality_profiles:
            qp_mapper = QualityProfileMapper(QualityProfileResource, ProfileFormatItemResource)
            definitions.append(
                ResourceDefinition(
                    name="quality_profiles",
                    order=4,
                    mapper=qp_mapper,
                    list_fn=lambda: client.quality_profiles.api_v3_qualityprofile_get(),
                    create_fn=lambda model: client.quality_profiles.api_v3_qualityprofile_post(
                        quality_profile_resource=model
                    ),
                    update_fn=lambda id, model: client.quality_profiles.api_v3_qualityprofile_id_put(
                        id=id, quality_profile_resource=model
                    ),
                    delete_fn=lambda id: client.quality_profiles.api_v3_qualityprofile_id_delete(
                        id=id
                    ),
                )
            )

        # 5. Delay Profiles (depends on tags)
        if instance_config.delay_profiles:
            dp_mapper = DelayProfileMapper(DelayProfileResource)
            definitions.append(
                ResourceDefinition(
                    name="delay_profiles",
                    order=5,
                    mapper=dp_mapper,
                    list_fn=lambda: client.delay_profiles.api_v3_delayprofile_get(),
                    create_fn=lambda model: client.delay_profiles.api_v3_delayprofile_post(
                        delay_profile_resource=model
                    ),
                    update_fn=lambda id, model: client.delay_profiles.api_v3_delayprofile_id_put(
                        id=id, delay_profile_resource=model
                    ),
                    delete_fn=lambda id: client.delay_profiles.api_v3_delayprofile_id_delete(id=id),
                )
            )

        # 6. Indexers (depends on tags)
        if instance_config.indexers:
            indexer_mapper = IndexerMapper(IndexerResource)
            definitions.append(
                ResourceDefinition(
                    name="indexers",
                    order=6,
                    mapper=indexer_mapper,
                    list_fn=lambda: client.indexers.api_v3_indexer_get(),
                    create_fn=lambda model: client.indexers.api_v3_indexer_post(
                        indexer_resource=model
                    ),
                    update_fn=lambda id, model: client.indexers.api_v3_indexer_id_put(
                        id=id, indexer_resource=model
                    ),
                    delete_fn=lambda id: client.indexers.api_v3_indexer_id_delete(id=id),
                )
            )

        # 7. Download Clients (depends on tags)
        if instance_config.download_clients:
            dc_mapper = DownloadClientMapper(DownloadClientResource)
            definitions.append(
                ResourceDefinition(
                    name="download_clients",
                    order=7,
                    mapper=dc_mapper,
                    list_fn=lambda: client.download_clients.api_v3_downloadclient_get(),
                    create_fn=lambda model: client.download_clients.api_v3_downloadclient_post(
                        download_client_resource=model
                    ),
                    update_fn=lambda id, model: client.download_clients.api_v3_downloadclient_id_put(
                        id=id, download_client_resource=model
                    ),
                    delete_fn=lambda id: client.download_clients.api_v3_downloadclient_id_delete(
                        id=id
                    ),
                )
            )

        # 8. Naming Config (singleton)
        if instance_config.naming:
            naming_mapper = NamingConfigMapper()
            definitions.append(
                ResourceDefinition(
                    name="naming",
                    order=8,
                    mapper=naming_mapper,
                    list_fn=lambda: [client.naming_config.get_naming_config()],
                    create_fn=lambda model: None,  # Singleton - no create
                    update_fn=lambda id, model: client.naming_config.update_naming_config(
                        id=id, naming_config_resource=model
                    ),
                    delete_fn=None,  # Singleton - no delete
                    is_singleton=True,
                )
            )

        # 9. Media Management Config (singleton)
        if instance_config.media_management:
            mm_mapper = MediaManagementConfigMapper()
            definitions.append(
                ResourceDefinition(
                    name="media_management",
                    order=9,
                    mapper=mm_mapper,
                    list_fn=lambda: [
                        client.media_management_config.api_v3_config_mediamanagement_get()
                    ],
                    create_fn=lambda model: None,  # Singleton - no create
                    update_fn=lambda id, model: client.media_management_config.api_v3_config_mediamanagement_id_put(
                        id=id, media_management_config_resource=model
                    ),
                    delete_fn=None,  # Singleton - no delete
                    is_singleton=True,
                )
            )

        return definitions

    def import_config(
        self,
        base_url: str,
        api_key: str,
        instance_name: str,
        mask_secrets: bool = True,
    ) -> dict[str, Any]:
        """Import configuration from a live Sonarr instance."""
        # This will be implemented by moving the existing import logic
        # For now, raise NotImplementedError as a placeholder
        raise NotImplementedError("Import functionality will be migrated")

    def create_backup(self, client: SonarrClient, backup_dir: str) -> dict[str, Any]:
        """Create a backup of current Sonarr state."""
        # This will be implemented by moving the existing backup logic
        # For now, raise NotImplementedError as a placeholder
        raise NotImplementedError("Backup functionality will be migrated")
