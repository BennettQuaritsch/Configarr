"""Environment configuration loader with support for .env files and env var interpolation."""

import os
import re
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def load_environment() -> None:
    """Load environment variables from .env file if it exists."""
    env_file = Path(".env")
    if env_file.exists():
        load_dotenv(env_file)


def interpolate_env_vars(value: str) -> str:
    """
    Replace ${VAR_NAME} or $VAR_NAME patterns in a string with environment variable values.

    Args:
        value: String potentially containing env var references

    Returns:
        String with all env vars resolved

    Raises:
        ValueError: If a referenced env var doesn't exist
    """
    if not isinstance(value, str):
        return value

    # Pattern matches ${VAR_NAME} or $VAR_NAME
    pattern = r"\$\{([^}]+)\}|\$([A-Za-z_][A-Za-z0-9_]*)"

    def replacer(match):
        var_name = match.group(1) or match.group(2)
        env_value = os.getenv(var_name)
        if env_value is None:
            raise ValueError(
                f"Environment variable '{var_name}' referenced in config but not found"
            )
        return env_value

    return re.sub(pattern, replacer, value)


def get_env_var(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """
    Get an environment variable value.

    Args:
        key: Environment variable name
        default: Default value if not found
        required: If True, raise ValueError when variable is missing

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required=True and variable not found
    """
    value = os.getenv(key, default)
    if required and value is None:
        raise ValueError(f"Required environment variable '{key}' not found")
    return value


def get_instance_config(prefix: str, instance_name: str) -> dict[str, str]:
    """
    Get configuration for a specific instance from environment variables.

    Looks for variables like:
    - {PREFIX}_{INSTANCE_NAME}_URL
    - {PREFIX}_{INSTANCE_NAME}_API_KEY

    Args:
        prefix: Service prefix (e.g., "SONARR")
        instance_name: Instance identifier (e.g., "MAIN", "ANIME")

    Returns:
        Dictionary with 'base_url' and 'api_key' keys

    Raises:
        ValueError: If required variables are missing
    """
    instance_upper = instance_name.upper().replace("-", "_")
    url_key = f"{prefix}_{instance_upper}_URL"
    api_key_key = f"{prefix}_{instance_upper}_API_KEY"

    base_url = get_env_var(url_key, required=True)
    api_key = get_env_var(api_key_key, required=True)

    return {"base_url": base_url, "api_key": api_key}
