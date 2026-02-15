"""Sonarr API client wrapper."""

from typing import Optional

from sonarr_api import ApiClient, Configuration
from sonarr_api.api.custom_format_api import CustomFormatApi
from sonarr_api.api.delay_profile_api import DelayProfileApi
from sonarr_api.api.download_client_api import DownloadClientApi
from sonarr_api.api.indexer_api import IndexerApi
from sonarr_api.api.media_management_config_api import MediaManagementConfigApi
from sonarr_api.api.naming_config_api import NamingConfigApi
from sonarr_api.api.ping_api import PingApi
from sonarr_api.api.quality_definition_api import QualityDefinitionApi
from sonarr_api.api.quality_profile_api import QualityProfileApi
from sonarr_api.api.tag_api import TagApi

from src.utils.logger import get_logger

logger = get_logger("sonarr_client")


class SonarrClient:
    """
    Wrapper around the generated Sonarr API client.

    Provides convenient access to all API endpoints and handles
    authentication configuration.
    """

    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the Sonarr client.

        Args:
            base_url: Sonarr server URL (e.g., "http://localhost:8989")
            api_key: API key for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

        # Configure API client
        self.config = Configuration(
            host=self.base_url,
            api_key={"X-Api-Key": self.api_key},
        )

        self._api_client: Optional[ApiClient] = None

        # API endpoint instances (lazy-loaded)
        self._custom_format_api: Optional[CustomFormatApi] = None
        self._quality_profile_api: Optional[QualityProfileApi] = None
        self._quality_definition_api: Optional[QualityDefinitionApi] = None
        self._tag_api: Optional[TagApi] = None
        self._delay_profile_api: Optional[DelayProfileApi] = None
        self._indexer_api: Optional[IndexerApi] = None
        self._download_client_api: Optional[DownloadClientApi] = None
        self._naming_config_api: Optional[NamingConfigApi] = None
        self._media_management_config_api: Optional[MediaManagementConfigApi] = None
        self._ping_api: Optional[PingApi] = None

    def __enter__(self):
        """Enter context manager."""
        self._api_client = ApiClient(self.config)
        self._api_client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        if self._api_client:
            self._api_client.__exit__(exc_type, exc_val, exc_tb)
            self._api_client = None

    @property
    def api_client(self) -> ApiClient:
        """Get the underlying API client."""
        if self._api_client is None:
            raise RuntimeError("Client not initialized. Use 'with' statement or call __enter__")
        return self._api_client

    # API endpoint properties with lazy initialization

    @property
    def custom_formats(self) -> CustomFormatApi:
        """Get the Custom Format API."""
        if self._custom_format_api is None:
            self._custom_format_api = CustomFormatApi(self.api_client)
        return self._custom_format_api

    @property
    def quality_profiles(self) -> QualityProfileApi:
        """Get the Quality Profile API."""
        if self._quality_profile_api is None:
            self._quality_profile_api = QualityProfileApi(self.api_client)
        return self._quality_profile_api

    @property
    def quality_definitions(self) -> QualityDefinitionApi:
        """Get the Quality Definition API."""
        if self._quality_definition_api is None:
            self._quality_definition_api = QualityDefinitionApi(self.api_client)
        return self._quality_definition_api

    @property
    def tags(self) -> TagApi:
        """Get the Tag API."""
        if self._tag_api is None:
            self._tag_api = TagApi(self.api_client)
        return self._tag_api

    @property
    def delay_profiles(self) -> DelayProfileApi:
        """Get the Delay Profile API."""
        if self._delay_profile_api is None:
            self._delay_profile_api = DelayProfileApi(self.api_client)
        return self._delay_profile_api

    @property
    def indexers(self) -> IndexerApi:
        """Get the Indexer API."""
        if self._indexer_api is None:
            self._indexer_api = IndexerApi(self.api_client)
        return self._indexer_api

    @property
    def download_clients(self) -> DownloadClientApi:
        """Get the Download Client API."""
        if self._download_client_api is None:
            self._download_client_api = DownloadClientApi(self.api_client)
        return self._download_client_api

    @property
    def naming_config(self) -> NamingConfigApi:
        """Get the Naming Config API."""
        if self._naming_config_api is None:
            self._naming_config_api = NamingConfigApi(self.api_client)
        return self._naming_config_api

    @property
    def media_management_config(self) -> MediaManagementConfigApi:
        """Get the Media Management Config API."""
        if self._media_management_config_api is None:
            self._media_management_config_api = MediaManagementConfigApi(self.api_client)
        return self._media_management_config_api

    @property
    def ping(self) -> PingApi:
        """Get the Ping API."""
        if self._ping_api is None:
            self._ping_api = PingApi(self.api_client)
        return self._ping_api

    def test_connection(self) -> bool:
        """
        Test the connection to Sonarr server.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self:
                response = self.ping.ping_get()
                logger.debug(f"Connection test successful: {response}")
                return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

    def get_server_info(self) -> dict:
        """
        Get basic server information.

        Returns:
            Dictionary with server info
        """
        try:
            with self:
                ping_response = self.ping.ping_get()
                # PingResource is a Pydantic model, convert to dict
                return {
                    "url": self.base_url,
                    "status": "online",
                    "version": getattr(ping_response, "version", "unknown"),
                }
        except Exception as e:
            logger.error(f"Failed to get server info: {e}")
            return {"url": self.base_url, "status": "error", "error": str(e)}
