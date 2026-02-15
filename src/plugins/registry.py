"""Plugin registry for discovering and managing Configarr plugins."""

from typing import Dict

from src.plugins.base import ArrPlugin
from src.plugins.sonarr.plugin import SonarrPlugin


class PluginRegistry:
    """Central registry for all *arr plugins."""

    def __init__(self):
        self._plugins: Dict[str, ArrPlugin] = {}
        self._register_builtin_plugins()

    def _register_builtin_plugins(self):
        """Register built-in plugins."""
        self.register(SonarrPlugin())

    def register(self, plugin: ArrPlugin):
        """
        Register a plugin.
        
        Args:
            plugin: Plugin instance to register
        """
        if plugin.name in self._plugins:
            raise ValueError(f"Plugin '{plugin.name}' is already registered")
        self._plugins[plugin.name] = plugin

    def get(self, name: str) -> ArrPlugin:
        """
        Get a plugin by name.
        
        Args:
            name: Plugin name (e.g., 'sonarr', 'radarr')
            
        Returns:
            Plugin instance
            
        Raises:
            KeyError: If plugin not found
        """
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not found. Available: {list(self._plugins.keys())}")
        return self._plugins[name]

    def get_all(self) -> Dict[str, ArrPlugin]:
        """Get all registered plugins."""
        return self._plugins.copy()

    def list_names(self) -> list[str]:
        """Get list of registered plugin names."""
        return list(self._plugins.keys())


# Global registry instance
_registry = PluginRegistry()


def get_registry() -> PluginRegistry:
    """Get the global plugin registry."""
    return _registry
