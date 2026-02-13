"""CLI entry point for Arr-Declarative-Manager (ADM)."""

import argparse
import sys
from pathlib import Path

from pydantic import ValidationError

from src.commands.import_config import import_sonarr_config
from src.core.config_schema import ADMConfig
from src.core.reconciler import Reconciler
from src.mapping.custom_formats import CustomFormatMapper
from src.mapping.delay_profiles import DelayProfileMapper
from src.mapping.download_clients import DownloadClientMapper
from src.mapping.indexers import IndexerMapper
from src.mapping.media_management import MediaManagementConfigMapper
from src.mapping.naming import NamingConfigMapper
from src.mapping.quality_definitions import QualityDefinitionMapper
from src.mapping.quality_profiles import QualityProfileMapper
from src.mapping.tags import TagMapper
from src.utils.backup import create_backup, cleanup_old_backups
from src.utils.env import get_instance_config, interpolate_env_vars, load_environment
from src.utils.logger import get_logger, setup_logger
from src.utils.sonarr_client import SonarrClient
from src.utils.yaml_loader import load_yaml_config


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Arr-Declarative-Manager - Configuration-as-code for Sonarr, Radarr, Prowlarr",
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

    # Import command
    import_parser = subparsers.add_parser(
        "import", help="Import existing Sonarr configuration to YAML"
    )
    import_parser.add_argument(
        "-u", "--url", required=True, help="Sonarr server URL (e.g., http://localhost:8989)"
    )
    import_parser.add_argument(
        "-k", "--api-key", required=True, help="Sonarr API key"
    )
    import_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("config/imported-sonarr.yaml"),
        help="Output file path (default: config/imported-sonarr.yaml)",
    )
    import_parser.add_argument(
        "-n",
        "--name",
        default="main-sonarr",
        help="Instance name in config (default: main-sonarr)",
    )
    import_parser.add_argument(
        "--include-secrets",
        action="store_true",
        help="Include API keys and passwords in output (NOT RECOMMENDED)",
    )
    import_parser.add_argument(
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
        config = ADMConfig(**raw_config)
        logger.info(f"✓ Config validation successful")
        logger.info(f"  Found {len(config.sonarr)} Sonarr instance(s)")

        for instance in config.sonarr:
            logger.info(f"    - {instance.name}")

        return 0

    except FileNotFoundError as e:
        logger.error(f"✗ Config file not found: {e}")
        return 1
    except ValidationError as e:
        logger.error(f"✗ Config validation failed:")
        for error in e.errors():
            loc = " -> ".join(str(l) for l in error["loc"])
            logger.error(f"    {loc}: {error['msg']}")
        return 1
    except Exception as e:
        logger.error(f"✗ Unexpected error: {e}")
        return 1


def sync_sonarr_instance(
    instance_config, dry_run: bool = False, no_backup: bool = False, logger=None
) -> bool:
    """
    Sync a single Sonarr instance.

    Returns:
        True on success, False on error
    """
    instance_name = instance_config.name

    logger.info(f"\n{'='*60}")
    logger.info(f"Syncing Sonarr instance: {instance_name}")
    logger.info(f"{'='*60}\n")

    # Get credentials
    base_url = instance_config.base_url
    api_key = instance_config.api_key

    # If not provided inline, try to load from env
    if not base_url or not api_key:
        try:
            env_config = get_instance_config("SONARR", instance_name)
            base_url = base_url or env_config["base_url"]
            api_key = api_key or env_config["api_key"]
        except ValueError as e:
            logger.error(f"✗ Failed to get credentials for instance '{instance_name}': {e}")
            return False

    # Initialize client
    client = SonarrClient(base_url=base_url, api_key=api_key)

    # Test connection
    logger.info(f"Testing connection to {base_url}...")
    if not client.test_connection():
        logger.error(f"✗ Connection test failed for instance '{instance_name}'")
        return False
    logger.info("✓ Connection successful\n")

    with client:
        # Create backup before sync (unless disabled or dry-run)
        if not dry_run and not no_backup:
            backup_dir = Path("backups")
            backup_file = create_backup(client, backup_dir, instance_name)
            if backup_file:
                # Clean up old backups (keep 5 most recent)
                cleanup_old_backups(backup_dir, keep_count=5)
            else:
                logger.warning("⚠ Failed to create backup, but continuing with sync...")

        # Build context maps (tag names -> IDs, custom format names -> IDs, etc.)
        context = _build_context(client, logger)

        # Sync resources in dependency order
        success = True

        # 1. Tags (no dependencies)
        if instance_config.tags:
            success &= _sync_tags(client, instance_config.tags, dry_run, logger)

            # Rebuild tag map after sync
            context["tag_map"] = _build_tag_map(client, logger)

        # 2. Custom Formats (no dependencies)
        if instance_config.custom_formats:
            success &= _sync_custom_formats(
                client, instance_config.custom_formats, dry_run, logger
            )

            # Rebuild custom format map after sync
            context["custom_format_map"] = _build_custom_format_map(client, logger)

        # 3. Quality Definitions (no dependencies)
        if instance_config.quality_definitions:
            success &= _sync_quality_definitions(
                client, instance_config.quality_definitions, dry_run, context, logger
            )

        # 4. Quality Profiles (depends on quality definitions + custom formats)
        if instance_config.quality_profiles:
            success &= _sync_quality_profiles(
                client, instance_config.quality_profiles, dry_run, context, logger
            )

        # 5. Delay Profiles (depends on tags)
        if instance_config.delay_profiles:
            success &= _sync_delay_profiles(
                client, instance_config.delay_profiles, dry_run, context, logger
            )

        # 6. Indexers (may depend on tags)
        if instance_config.indexers:
            success &= _sync_indexers(client, instance_config.indexers, dry_run, context, logger)

        # 7. Download Clients (may depend on tags)
        if instance_config.download_clients:
            success &= _sync_download_clients(
                client, instance_config.download_clients, dry_run, context, logger
            )

        # 8. Naming Config (singleton)
        if instance_config.naming:
            success &= _sync_naming_config(client, instance_config.naming, dry_run, logger)

        # 9. Media Management (singleton)
        if instance_config.media_management:
            success &= _sync_media_management(
                client, instance_config.media_management, dry_run, logger
            )

    if success:
        logger.info(f"\n✓ Successfully synced instance: {instance_name}\n")
    else:
        logger.warning(f"\n⚠ Instance sync completed with errors: {instance_name}\n")

    return success


def _build_context(client: SonarrClient, logger) -> dict:
    """Build context maps for cross-resource references."""
    return {
        "tag_map": _build_tag_map(client, logger),
        "custom_format_map": _build_custom_format_map(client, logger),
    }


def _build_tag_map(client: SonarrClient, logger) -> dict[str, int]:
    """Build a map of tag name -> tag ID."""
    tags = client.tags.api_v3_tag_get()
    tag_map = {tag.label: tag.id for tag in tags}
    logger.debug(f"Built tag map: {len(tag_map)} tags")
    return tag_map


def _build_custom_format_map(client: SonarrClient, logger) -> dict[str, int]:
    """Build a map of custom format name -> ID."""
    formats = client.custom_formats.api_v3_customformat_get()
    cf_map = {cf.name: cf.id for cf in formats}
    logger.debug(f"Built custom format map: {len(cf_map)} formats")
    return cf_map


def _sync_tags(client, tags_config, dry_run, logger) -> bool:
    """Sync tags."""
    try:
        mapper = TagMapper()
        reconciler = Reconciler(
            resource_name="Tag",
            mapper=mapper,
            list_fn=lambda: client.tags.api_v3_tag_get(),
            create_fn=lambda model: client.tags.api_v3_tag_post(tag_resource=model),
            update_fn=lambda id, model: client.tags.api_v3_tag_id_put(id=str(id), tag_resource=model),
            delete_fn=lambda id: client.tags.api_v3_tag_id_delete(id=id),
        )

        reconciler.reconcile(
            desired=tags_config.definitions,
            delete_unmanaged=tags_config.delete_unmanaged,
            dry_run=dry_run,
        )
        return True
    except Exception as e:
        logger.error(f"Error syncing tags: {e}")
        return False


def _sync_custom_formats(client, cf_config, dry_run, logger) -> bool:
    """Sync custom formats."""
    try:
        mapper = CustomFormatMapper()
        reconciler = Reconciler(
            resource_name="Custom Format",
            mapper=mapper,
            list_fn=lambda: client.custom_formats.api_v3_customformat_get(),
            create_fn=lambda model: client.custom_formats.api_v3_customformat_post(
                custom_format_resource=model
            ),
            update_fn=lambda id, model: client.custom_formats.api_v3_customformat_id_put(
                id=str(id), custom_format_resource=model
            ),
            delete_fn=lambda id: client.custom_formats.api_v3_customformat_id_delete(id=id),
        )

        reconciler.reconcile(
            desired=cf_config.definitions,
            delete_unmanaged=cf_config.delete_unmanaged,
            dry_run=dry_run,
        )
        return True
    except Exception as e:
        logger.error(f"Error syncing custom formats: {e}")
        return False


def _sync_quality_definitions(client, qd_config, dry_run, context, logger) -> bool:
    """Sync quality definitions."""
    try:
        mapper = QualityDefinitionMapper()

        # Quality definitions can't be created/deleted, only updated
        # So we use a custom approach instead of the generic reconciler
        current_defs = client.quality_definitions.api_v3_qualitydefinition_get()
        current_map = {qd.title: qd for qd in current_defs}

        for yaml_def in qd_config.definitions:
            if yaml_def.title not in current_map:
                logger.warning(f"Quality definition '{yaml_def.title}' not found on server, skipping")
                continue

            existing = current_map[yaml_def.title]
            api_model = mapper.to_api_model(yaml_def, existing_definition=existing)

            current_dict = mapper.from_api_model(existing)
            desired_dict = mapper.from_api_model(api_model)

            if mapper.needs_update(current_dict, desired_dict):
                if dry_run:
                    logger.info(f"[DRY RUN] Would update Quality Definition: {yaml_def.title}")
                else:
                    logger.info(f"Updating Quality Definition: {yaml_def.title}")
                    client.quality_definitions.api_v3_qualitydefinition_id_put(
                        id=str(existing.id), quality_definition_resource=api_model
                    )
                    logger.info(f"✓ Updated Quality Definition: {yaml_def.title}")

        return True
    except Exception as e:
        logger.error(f"Error syncing quality definitions: {e}")
        return False


def _sync_quality_profiles(client, qp_config, dry_run, context, logger) -> bool:
    """Sync quality profiles."""
    try:
        mapper = QualityProfileMapper()
        reconciler = Reconciler(
            resource_name="Quality Profile",
            mapper=mapper,
            list_fn=lambda: client.quality_profiles.api_v3_qualityprofile_get(),
            create_fn=lambda model: client.quality_profiles.api_v3_qualityprofile_post(
                quality_profile_resource=model
            ),
            update_fn=lambda id, model: client.quality_profiles.api_v3_qualityprofile_id_put(
                id=str(id), quality_profile_resource=model
            ),
            delete_fn=lambda id: client.quality_profiles.api_v3_qualityprofile_id_delete(id=id),
        )

        reconciler.reconcile(
            desired=qp_config.definitions,
            delete_unmanaged=qp_config.delete_unmanaged,
            dry_run=dry_run,
            context=context,
        )
        return True
    except Exception as e:
        logger.error(f"Error syncing quality profiles: {e}")
        return False


def _sync_delay_profiles(client, dp_config, dry_run, context, logger) -> bool:
    """Sync delay profiles."""
    try:
        mapper = DelayProfileMapper()
        reconciler = Reconciler(
            resource_name="Delay Profile",
            mapper=mapper,
            list_fn=lambda: client.delay_profiles.api_v3_delayprofile_get(),
            create_fn=lambda model: client.delay_profiles.api_v3_delayprofile_post(
                delay_profile_resource=model
            ),
            update_fn=lambda id, model: client.delay_profiles.api_v3_delayprofile_id_put(
                id=str(id), delay_profile_resource=model
            ),
            delete_fn=lambda id: client.delay_profiles.api_v3_delayprofile_id_delete(id=id),
        )

        reconciler.reconcile(
            desired=dp_config.definitions,
            delete_unmanaged=dp_config.delete_unmanaged,
            dry_run=dry_run,
            context=context,
        )
        return True
    except Exception as e:
        logger.error(f"Error syncing delay profiles: {e}")
        return False


def _sync_indexers(client, indexer_config, dry_run, context, logger) -> bool:
    """Sync indexers."""
    try:
        mapper = IndexerMapper()
        reconciler = Reconciler(
            resource_name="Indexer",
            mapper=mapper,
            list_fn=lambda: client.indexers.api_v3_indexer_get(),
            create_fn=lambda model: client.indexers.api_v3_indexer_post(indexer_resource=model),
            update_fn=lambda id, model: client.indexers.api_v3_indexer_id_put(
                id=str(id), indexer_resource=model
            ),
            delete_fn=lambda id: client.indexers.api_v3_indexer_id_delete(id=id),
        )

        reconciler.reconcile(
            desired=indexer_config.definitions,
            delete_unmanaged=indexer_config.delete_unmanaged,
            dry_run=dry_run,
            context=context,
        )
        return True
    except Exception as e:
        logger.error(f"Error syncing indexers: {e}")
        return False


def _sync_download_clients(client, dc_config, dry_run, context, logger) -> bool:
    """Sync download clients."""
    try:
        mapper = DownloadClientMapper()
        reconciler = Reconciler(
            resource_name="Download Client",
            mapper=mapper,
            list_fn=lambda: client.download_clients.api_v3_downloadclient_get(),
            create_fn=lambda model: client.download_clients.api_v3_downloadclient_post(
                download_client_resource=model
            ),
            update_fn=lambda id, model: client.download_clients.api_v3_downloadclient_id_put(
                id=str(id), download_client_resource=model
            ),
            delete_fn=lambda id: client.download_clients.api_v3_downloadclient_id_delete(id=id),
        )

        reconciler.reconcile(
            desired=dc_config.definitions,
            delete_unmanaged=dc_config.delete_unmanaged,
            dry_run=dry_run,
            context=context,
        )
        return True
    except Exception as e:
        logger.error(f"Error syncing download clients: {e}")
        return False


def _sync_naming_config(client, naming_config, dry_run, logger) -> bool:
    """Sync naming configuration."""
    try:
        mapper = NamingConfigMapper()

        # Naming config is a singleton - fetch existing
        existing = client.naming_config.api_v3_config_naming_get()
        api_model = mapper.to_api_model(naming_config, existing_config=existing)

        current_dict = mapper.from_api_model(existing)
        desired_dict = mapper.from_api_model(api_model)

        if mapper.needs_update(current_dict, desired_dict):
            if dry_run:
                logger.info("[DRY RUN] Would update Naming Config")
            else:
                logger.info("Updating Naming Config")
                client.naming_config.api_v3_config_naming_id_put(
                    id=str(existing.id), naming_config_resource=api_model
                )
                logger.info("✓ Updated Naming Config")
        else:
            logger.info("Naming Config: no changes needed")

        return True
    except Exception as e:
        logger.error(f"Error syncing naming config: {e}")
        return False


def _sync_media_management(client, mm_config, dry_run, logger) -> bool:
    """Sync media management configuration."""
    try:
        mapper = MediaManagementConfigMapper()

        # Media management config is a singleton - fetch existing
        existing = client.media_management_config.api_v3_config_mediamanagement_get()
        api_model = mapper.to_api_model(mm_config, existing_config=existing)

        current_dict = mapper.from_api_model(existing)
        desired_dict = mapper.from_api_model(api_model)

        if mapper.needs_update(current_dict, desired_dict):
            if dry_run:
                logger.info("[DRY RUN] Would update Media Management Config")
            else:
                logger.info("Updating Media Management Config")
                client.media_management_config.api_v3_config_mediamanagement_id_put(
                    id=str(existing.id), media_management_config_resource=api_model
                )
                logger.info("✓ Updated Media Management Config")
        else:
            logger.info("Media Management Config: no changes needed")

        return True
    except Exception as e:
        logger.error(f"Error syncing media management: {e}")
        return False


def sync_config(
    config_path: Path, dry_run: bool = False, no_backup: bool = False, verbose: bool = False
) -> int:
    """
    Sync configuration to servers.

    Returns:
        0 on success, 1 on error
    """
    logger = setup_logger(verbose=verbose)

    # Load environment variables
    load_environment()

    logger.info(f"Loading config: {config_path}")
    if dry_run:
        logger.info("[DRY RUN MODE] No changes will be applied\n")

    try:
        # Load and validate config
        raw_config = load_yaml_config(config_path)
        config = ADMConfig(**raw_config)

        # Sync each Sonarr instance
        all_success = True
        for instance_config in config.sonarr:
            success = sync_sonarr_instance(
                instance_config, dry_run=dry_run, no_backup=no_backup, logger=logger
            )
            all_success &= success

        if all_success:
            logger.info("\n✓ All instances synced successfully")
            return 0
        else:
            logger.warning("\n⚠ Some instances had errors")
            return 1

    except Exception as e:
        logger.error(f"✗ Sync failed: {e}")
        if verbose:
            import traceback

            traceback.print_exc()
        return 1


def main() -> int:
    """Main entry point."""
    args = parse_args()

    if not args.command:
        print("Error: No command specified. Use 'adm --help' for usage.")
        return 1

    if args.command == "validate":
        return validate_config(args.config, verbose=args.verbose)
    elif args.command == "sync":
        return sync_config(
            args.config,
            dry_run=args.dry_run,
            no_backup=args.no_backup,
            verbose=args.verbose,
        )
    elif args.command == "import":
        logger = setup_logger(verbose=args.verbose)
        load_environment()
        success = import_sonarr_config(
            base_url=args.url,
            api_key=args.api_key,
            output_path=args.output,
            instance_name=args.name,
            include_secrets=args.include_secrets,
        )
        return 0 if success else 1

    return 1


if __name__ == "__main__":
    sys.exit(main())
