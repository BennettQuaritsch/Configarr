"""Custom YAML loader with support for !include directive."""

import os
from pathlib import Path
from typing import Any

import yaml

from src.utils.env import interpolate_env_vars


class IncludeLoader(yaml.SafeLoader):
    """YAML loader with !include tag support."""

    def __init__(self, stream):
        """Initialize loader with the file path for resolving relative includes."""
        self._root = Path(stream.name).parent if hasattr(stream, "name") else Path.cwd()
        super().__init__(stream)


def include_constructor(loader: IncludeLoader, node: yaml.Node) -> Any:
    """
    Handle !include tag in YAML files.

    Supports:
    - !include path/to/file.yaml  (loads and merges the file)
    - Relative paths are resolved from the parent YAML file's directory
    """
    include_path = loader.construct_scalar(node)

    # Resolve relative to the current file's directory
    full_path = loader._root / include_path

    if not full_path.exists():
        raise FileNotFoundError(f"Included file not found: {full_path}")

    with open(full_path, "r") as include_file:
        return yaml.load(include_file, IncludeLoader)


# Register the !include constructor
IncludeLoader.add_constructor("!include", include_constructor)


def load_yaml_config(config_path: Path | str) -> dict:
    """
    Load a YAML config file with !include support and env var interpolation.

    Args:
        config_path: Path to the YAML config file

    Returns:
        Parsed config dictionary

    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If YAML parsing fails
        ValueError: If referenced env vars don't exist
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as f:
        raw_config = yaml.load(f, IncludeLoader)

    # Recursively interpolate env vars in the loaded config
    return _interpolate_recursive(raw_config)


def _interpolate_recursive(obj: Any) -> Any:
    """
    Recursively traverse a config object and interpolate env vars in all strings.

    Args:
        obj: Config object (dict, list, str, or primitive)

    Returns:
        Config object with all env vars interpolated
    """
    if isinstance(obj, dict):
        return {key: _interpolate_recursive(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [_interpolate_recursive(item) for item in obj]
    elif isinstance(obj, str):
        return interpolate_env_vars(obj)
    else:
        return obj


def save_yaml_config(config: dict, output_path: Path | str) -> None:
    """
    Save a config dictionary to a YAML file.

    Args:
        config: Configuration dictionary
        output_path: Path to write the YAML file
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        yaml.dump(
            config,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            indent=2,
        )
