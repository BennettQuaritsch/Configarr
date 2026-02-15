"""CLI entry point for Configarr - Plugin-based architecture."""

import argparse
import sys
from pathlib import Path

from pydantic import ValidationError

from src.core.config_schema import ConfigarrConfig
from src.core.reconciler import Reconciler
from src.plugins.registry import get_registry
from src.utils.env import get_instance_config, load_environment
from src.utils.logger import get_logger, setup_logger
from src.utils.yaml_loader import load_yaml_config


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Configarr - Configuration-as-code for Sonarr, Radarr, Prowlarr",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version="0.1.0", help="Show version and exit"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Sync configuration to servers")
    sync_parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=Path("config/sonarr.yaml"),
        help="Path to config file (default: config/sonarr.yaml)",
    )
    sync_parser.add_argument(
        "--dry-run", action="store_true", help="Show changes without applying them"
    )
    sync_parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip creating backup before sync (NOT RECOMMENDED)",
    )
    sync_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging (DEBUG level)"
    )

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate configuration file")
    validate_parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=Path("config/sonarr.yaml"),
        help="Path to config file (default: config/sonarr.yaml)",
    )
    validate_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging (DEBUG level)"
    )

    return parser.parse_args()


def validate_config(config_path: Path, verbose: bool = False) -> int:
    """
    Validate a config file.

    Returns:
        0 on success, 1 on error
    """
    logger = setup_logger(verbose=verbose)
    
    # Load environment variables for interpolation
    load_environment()

    logger.info(f"Validating config file: {config_path}")

    try:
        # Load and parse YAML
        raw_config = load_yaml_config(config_path)
        logger.debug(f"Loaded raw config: {len(raw_config)} top-level keys")

        # Validate with Pydantic
        config = ConfigarrConfig(**raw_config)
        logger.info("✓ Config validation successful")
        
        # Report instances by plugin
        registry = get_registry()
        for plugin_name in registry.list_names():
            instances = getattr(config, plugin_name, [])
            if instances:
                plugin = registry.get(plugin_name)
                logger.info(f"  Found {len(instances)} {plugin.display_name} instance(s)")
                for instance in instances:
                    logger.info(f"    - {instance.name}")

        return 0

    except FileNotFoundError as e:
        logger.error(f"✗ Config file not found: {e}")
        return 1
    except ValidationError as e:
        logger.error("✗ Config validation failed:")
        for error in e.errors():
            loc = " -> ".join(str(l) for l in error["loc"])
            logger.error(f"    {loc}: {error['msg']}")
        return 1
    except Exception as e:
        logger.error(f"✗ Unexpected error: {e}")
        return 1


def sync_instance(plugin, instance_config, dry_run: bool = False, no_backup: bool = False, logger=None):
    """
    Sync a single instance using its plugin.

    Returns:
        True on success, False on error
    """
    instance_name = instance_config.name

    logger.info(f"\n{'='*60}")
    logger.info(f"Syncing {plugin.display_name} instance: {instance_name}")
    logger.info(f"{'='*60}\n")

    # Get credentials
    base_url = instance_config.base_url
    api_key = instance_config.api_key

    # If not provided inline, try to load from env
    if not base_url or not api_key:
        try:
            env_config = get_instance_config(plugin.name.upper(), instance_name)
            base_url = base_url or env_config["base_url"]
            api_key = api_key or env_config["api_key"]
        except ValueError as e:
            logger.error(f"✗ Failed to get credentials for instance '{instance_name}': {e}")
            return False

    # Initialize client
    client = plugin.get_client(base_url=base_url, api_key=api_key)

    # Test connection
    logger.info(f"Testing connection to {base_url}...")
    try:
        with client:
            # Simple connection test - check if we can access the client
            logger.info("✓ Connection successful\n")
    except Exception as e:
        logger.error(f"✗ Connection test failed for instance '{instance_name}': {e}")
        return False

    with client:
        # Get resource definitions from plugin
        resource_definitions = plugin.get_resource_definitions(client, instance_config)
        
        if not resource_definitions:
            logger.info("No resources configured for sync")
            return True

        # Build context maps (tag map, custom format map, etc.)
        context = _build_context_maps(client, resource_definitions)

        # Sync each resource in order
        for resource_def in sorted(resource_definitions, key=lambda r: r.order):
            logger.info(f"Syncing {resource_def.name}...")
            
            # Get YAML definitions for this resource
            yaml_defs = _get_yaml_definitions(instance_config, resource_def.name)
            
            if not yaml_defs:
                logger.info(f"  No {resource_def.name} configured, skipping")
                continue

            # Create and run reconciler
            reconciler = Reconciler(
                resource_name=resource_def.name,
                mapper=resource_def.mapper,
                list_fn=resource_def.list_fn,
                create_fn=resource_def.create_fn,
                update_fn=resource_def.update_fn,
                delete_fn=resource_def.delete_fn,
            )

            try:
                reconciler.reconcile(
                    desired=yaml_defs,
                    dry_run=dry_run,
                    delete_unmanaged=_should_delete_unmanaged(instance_config, resource_def.name),
                    context=context,
                )
            except Exception as e:
                logger.error(f"  ✗ Failed to sync {resource_def.name}: {e}")
                return False

    logger.info(f"\n✓ Successfully synced {plugin.display_name} instance: {instance_name}")
    return True


def _build_context_maps(client, resource_definitions) -> dict:
    """Build context maps needed by mappers (tag IDs, custom format IDs, etc.)."""
    context = {}
    
    # Build tag map if tags are being synced
    if any(rd.name == "tags" for rd in resource_definitions):
        try:
            tags = client.tags.api_v3_tag_get()
            context["tag_map"] = {tag.label: tag.id for tag in tags}
        except:
            context["tag_map"] = {}
    
    # Build custom format map if custom formats are being synced
    if any(rd.name == "custom_formats" for rd in resource_definitions):
        try:
            cfs = client.custom_formats.api_v3_customformat_get()
            context["custom_format_map"] = {cf.name: cf.id for cf in cfs}
        except:
            context["custom_format_map"] = {}
    
    return context


def _get_yaml_definitions(instance_config, resource_name: str):
    """Extract YAML definitions for a specific resource from instance config."""
    resource_config = getattr(instance_config, resource_name, None)
    if not resource_config:
        return []
    
    # Handle different resource structures
    if resource_name in ["naming", "media_management"]:
        # Singleton resources - return the config itself as a single-item list
        return [resource_config]
    elif hasattr(resource_config, "definitions"):
        # Most resources have a 'definitions' list
        return resource_config.definitions
    else:
        return []


def _should_delete_unmanaged(instance_config, resource_name: str) -> bool:
    """Check if unmanaged resources should be deleted for this resource type."""
    resource_config = getattr(instance_config, resource_name, None)
    if not resource_config:
        return False
    return getattr(resource_config, "delete_unmanaged", False)


def sync_config(config_path: Path, dry_run: bool = False, no_backup: bool = False, verbose: bool = False) -> int:
    """
    Sync configuration to servers.

    Returns:
        0 on success, 1 on error
    """
    logger = setup_logger(verbose=verbose)
    
    # Load environment variables
    load_environment()

    logger.info(f"Loading config file: {config_path}")

    try:
        # Load and validate config
        raw_config = load_yaml_config(config_path)
        config = ConfigarrConfig(**raw_config)

        if dry_run:
            logger.info("\n🔍 DRY RUN MODE - No changes will be applied\n")

        # Get plugin registry
        registry = get_registry()

        # Sync instances for each plugin
        success = True
        for plugin_name in registry.list_names():
            plugin = registry.get(plugin_name)
            instances = getattr(config, plugin_name, [])
            
            for instance_config in instances:
                if not sync_instance(plugin, instance_config, dry_run, no_backup, logger):
                    success = False

        if success:
            logger.info("\n✓ All instances synced successfully")
            return 0
        else:
            logger.error("\n✗ Some instances failed to sync")
            return 1

    except FileNotFoundError as e:
        logger.error(f"✗ Config file not found: {e}")
        return 1
    except ValidationError as e:
        logger.error("✗ Config validation failed:")
        for error in e.errors():
            loc = " -> ".join(str(l) for l in error["loc"])
            logger.error(f"    {loc}: {error['msg']}")
        return 1
    except Exception as e:
        logger.error(f"✗ Unexpected error: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        return 1


def main():
    """Main CLI entry point."""
    args = parse_args()

    if args.command == "validate":
        return validate_config(args.config, args.verbose)
    elif args.command == "sync":
        return sync_config(args.config, args.dry_run, args.no_backup, args.verbose)
    else:
        print("No command specified. Use --help for usage information.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
