"""Base classes and protocols for the Configarr plugin system."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Protocol

from pydantic import BaseModel


class ArrClient(Protocol):
    """
    Protocol defining the interface for *arr application API clients.
    
    Clients must be context managers that provide access to various API endpoints.
    The specific endpoint properties are defined by each implementation (e.g., SonarrClient).
    """

    def __enter__(self) -> "ArrClient":
        """Enter the context manager."""
        ...

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager."""
        ...


@dataclass
class ResourceDefinition:
    """
    Bundles all information needed to reconcile a single resource type.
    
    Attributes:
        name: Resource type name (e.g., "tags", "custom_formats")
        order: Sync order priority (lower numbers sync first)
        mapper: ResourceMapper instance for this resource
        list_fn: Callable that returns list of current resources from API
        create_fn: Callable that creates a new resource via API
        update_fn: Callable that updates an existing resource via API
        delete_fn: Callable that deletes a resource via API (None for singleton resources)
        is_singleton: Whether this resource has only one instance (e.g., naming config)
    """

    name: str
    order: int
    mapper: Any  # ResourceMapper - avoiding import cycle
    list_fn: Callable[[], list]
    create_fn: Callable[[Any], Any]
    update_fn: Callable[[str, Any], Any]
    delete_fn: Callable[[str], None] | None = None
    is_singleton: bool = False


class ArrPlugin(ABC):
    """
    Abstract base class for *arr application plugins.
    
    Each plugin (Sonarr, Radarr, etc.) implements this interface to provide
    app-specific configuration, API client, mappers, and reconciliation logic.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin identifier (e.g., 'sonarr', 'radarr')."""
        pass

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-readable name (e.g., 'Sonarr', 'Radarr')."""
        pass

    @property
    @abstractmethod
    def config_key(self) -> str:
        """YAML root-level key for this plugin's instances (e.g., 'sonarr')."""
        pass

    @abstractmethod
    def get_client(self, base_url: str, api_key: str) -> ArrClient:
        """
        Create an API client for this plugin.
        
        Args:
            base_url: Server URL
            api_key: API authentication key
            
        Returns:
            Configured API client instance
        """
        pass

    @abstractmethod
    def get_instance_schema(self) -> type[BaseModel]:
        """
        Get the Pydantic model class for validating instance configuration.
        
        Returns:
            Pydantic BaseModel subclass for this plugin's instance config
        """
        pass

    @abstractmethod
    def get_resource_definitions(
        self, client: ArrClient, instance_config: BaseModel
    ) -> list[ResourceDefinition]:
        """
        Build the ordered list of resource definitions to reconcile.
        
        Args:
            client: API client instance
            instance_config: Validated instance configuration
            
        Returns:
            List of ResourceDefinition objects in sync order
        """
        pass

    @abstractmethod
    def import_config(
        self,
        base_url: str,
        api_key: str,
        instance_name: str,
        mask_secrets: bool = True,
    ) -> dict[str, Any]:
        """
        Import existing configuration from a live server into YAML-compatible dict.
        
        Args:
            base_url: Server URL
            api_key: API authentication key
            instance_name: Name for this instance in the generated config
            mask_secrets: Whether to replace secrets with env var placeholders
            
        Returns:
            Dictionary representing the instance configuration
        """
        pass

    @abstractmethod
    def create_backup(self, client: ArrClient, backup_dir: str) -> dict[str, Any]:
        """
        Create a backup of current server state.
        
        Args:
            client: API client instance
            backup_dir: Directory path where backup should be saved
            
        Returns:
            Dictionary containing the backup data
        """
        pass
