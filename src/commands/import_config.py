"""Import existing Sonarr configuration to YAML format."""

from pathlib import Path
from typing import Any

import yaml

from src.utils.logger import get_logger
from src.utils.sonarr_client import SonarrClient

logger = get_logger("import")


def import_sonarr_config(
    base_url: str,
    api_key: str,
    output_path: Path,
    instance_name: str = "main-sonarr",
    include_secrets: bool = False,
) -> bool:
    """
    Import existing Sonarr configuration and generate a YAML config file.

    Args:
        base_url: Sonarr server URL
        api_key: Sonarr API key
        output_path: Path to write YAML config
        instance_name: Name for this instance in the config
        include_secrets: If True, include API keys and passwords in output

    Returns:
        True on success, False on error
    """
    logger.info(f"Connecting to Sonarr at {base_url}...")

    client = SonarrClient(base_url=base_url, api_key=api_key)

    if not client.test_connection():
        logger.error("Failed to connect to Sonarr")
        return False

    logger.info("✓ Connected successfully")

    config = {
        "sonarr_instances": [
            {
                "name": instance_name,
                "base_url": base_url if include_secrets else "${SONARR_MAIN_URL}",
                "api_key": api_key if include_secrets else "${SONARR_MAIN_API_KEY}",
            }
        ]
    }

    instance_config: dict[str, Any] = {}

    with client:
        # Import Tags
        logger.info("Importing tags...")
        tags = client.tags.api_v3_tag_get()
        if tags:
            instance_config["tags"] = {
                "items": [{"name": tag.label} for tag in tags],
                "delete_unmanaged": False,
            }
            logger.info(f"  Found {len(tags)} tag(s)")

        # Import Custom Formats
        logger.info("Importing custom formats...")
        custom_formats = client.custom_formats.api_v3_customformat_get()
        if custom_formats:
            cf_items = []
            for cf in custom_formats:
                cf_dict = {
                    "name": cf.name,
                    "include_when_renaming": cf.include_custom_format_when_renaming,
                }
                if cf.specifications:
                    cf_dict["specifications"] = [
                        _serialize_specification(spec) for spec in cf.specifications
                    ]
                cf_items.append(cf_dict)

            instance_config["custom_formats"] = {
                "items": cf_items,
                "delete_unmanaged": False,
            }
            logger.info(f"  Found {len(custom_formats)} custom format(s)")

        # Import Quality Definitions
        logger.info("Importing quality definitions...")
        quality_defs = client.quality_definitions.api_v3_qualitydefinition_get()
        if quality_defs:
            qd_items = []
            for qd in quality_defs:
                qd_items.append(
                    {
                        "name": qd.title,
                        "min_size": qd.min_size,
                        "max_size": qd.max_size,
                        "preferred_size": qd.preferred_size,
                    }
                )

            instance_config["quality_definitions"] = {
                "items": qd_items,
            }
            logger.info(f"  Found {len(quality_defs)} quality definition(s)")

        # Import Quality Profiles
        logger.info("Importing quality profiles...")
        quality_profiles = client.quality_profiles.api_v3_qualityprofile_get()
        if quality_profiles:
            qp_items = []
            for qp in quality_profiles:
                qp_dict = {
                    "name": qp.name,
                    "upgrade_allowed": qp.upgrade_allowed,
                    "cutoff": qp.cutoff,
                    "items": _serialize_quality_items(qp.items),
                }

                # Add format items (custom format scores)
                if qp.format_items:
                    qp_dict["format_items"] = [
                        {"name": fi.name, "score": fi.score} for fi in qp.format_items
                    ]

                if qp.min_format_score is not None:
                    qp_dict["min_format_score"] = qp.min_format_score
                if qp.cutoff_format_score is not None:
                    qp_dict["cutoff_format_score"] = qp.cutoff_format_score

                qp_items.append(qp_dict)

            instance_config["quality_profiles"] = {
                "items": qp_items,
                "delete_unmanaged": False,
            }
            logger.info(f"  Found {len(quality_profiles)} quality profile(s)")

        # Import Delay Profiles
        logger.info("Importing delay profiles...")
        delay_profiles = client.delay_profiles.api_v3_delayprofile_get()
        if delay_profiles:
            dp_items = []
            for dp in delay_profiles:
                dp_dict = {
                    "enable_usenet": dp.enable_usenet,
                    "enable_torrent": dp.enable_torrent,
                    "preferred_protocol": dp.preferred_protocol,
                    "usenet_delay": dp.usenet_delay,
                    "torrent_delay": dp.torrent_delay,
                    "bypass_if_highest_quality": dp.bypass_if_highest_quality,
                }

                # Add tags if present
                if dp.tags:
                    tag_names = [
                        tag.label for tag in tags if tag.id in dp.tags
                    ]
                    if tag_names:
                        dp_dict["tags"] = tag_names

                # Add order for non-default profiles
                if dp.order != 2147483647:  # Default profile has max int order
                    dp_dict["order"] = dp.order

                dp_items.append(dp_dict)

            instance_config["delay_profiles"] = {
                "items": dp_items,
                "delete_unmanaged": False,
            }
            logger.info(f"  Found {len(delay_profiles)} delay profile(s)")

        # Import Indexers
        logger.info("Importing indexers...")
        indexers = client.indexers.api_v3_indexer_get()
        if indexers:
            idx_items = []
            for idx in indexers:
                idx_dict = {
                    "name": idx.name,
                    "enable_rss": idx.enable_rss,
                    "enable_automatic_search": idx.enable_automatic_search,
                    "enable_interactive_search": idx.enable_interactive_search,
                    "priority": idx.priority,
                    "implementation": idx.implementation,
                    "config_contract": idx.config_contract,
                }

                # Add protocol if present
                if idx.protocol:
                    idx_dict["protocol"] = idx.protocol

                # Add fields (sanitize secrets if needed)
                if idx.fields:
                    idx_dict["fields"] = _serialize_fields(idx.fields, include_secrets)

                # Add tags if present
                if idx.tags:
                    tag_names = [
                        tag.label for tag in tags if tag.id in idx.tags
                    ]
                    if tag_names:
                        idx_dict["tags"] = tag_names

                idx_items.append(idx_dict)

            instance_config["indexers"] = {
                "items": idx_items,
                "delete_unmanaged": False,
            }
            logger.info(f"  Found {len(indexers)} indexer(s)")

        # Import Download Clients
        logger.info("Importing download clients...")
        download_clients = client.download_clients.api_v3_downloadclient_get()
        if download_clients:
            dc_items = []
            for dc in download_clients:
                dc_dict = {
                    "name": dc.name,
                    "enable": dc.enable,
                    "priority": dc.priority,
                    "implementation": dc.implementation,
                    "config_contract": dc.config_contract,
                }

                # Add protocol if present
                if dc.protocol:
                    dc_dict["protocol"] = dc.protocol

                # Add fields (sanitize secrets if needed)
                if dc.fields:
                    dc_dict["fields"] = _serialize_fields(dc.fields, include_secrets)

                # Add tags if present
                if dc.tags:
                    tag_names = [
                        tag.label for tag in tags if tag.id in dc.tags
                    ]
                    if tag_names:
                        dc_dict["tags"] = tag_names

                dc_items.append(dc_dict)

            instance_config["download_clients"] = {
                "items": dc_items,
                "delete_unmanaged": False,
            }
            logger.info(f"  Found {len(download_clients)} download client(s)")

        # Import Naming Config
        logger.info("Importing naming configuration...")
        naming = client.naming_config.get_naming_config()
        if naming:
            instance_config["naming"] = {
                "rename_episodes": naming.rename_episodes,
                "replace_illegal_characters": naming.replace_illegal_characters,
                "standard_episode_format": naming.standard_episode_format,
                "daily_episode_format": naming.daily_episode_format,
                "anime_episode_format": naming.anime_episode_format,
                "series_folder_format": naming.series_folder_format,
                "season_folder_format": naming.season_folder_format,
                "specials_folder_format": naming.specials_folder_format,
            }
            logger.info("  ✓ Imported naming config")

        # Import Media Management Config
        logger.info("Importing media management configuration...")
        media_mgmt = client.media_management_config.get_media_management_config()
        if media_mgmt:
            instance_config["media_management"] = {
                "auto_unmonitor_previously_downloaded_episodes": media_mgmt.auto_unmonitor_previously_downloaded_episodes,
                "recycle_bin": media_mgmt.recycle_bin,
                "recycle_bin_cleanup_days": media_mgmt.recycle_bin_cleanup_days,
                "download_propers_and_repacks": media_mgmt.download_propers_and_repacks,
                "create_empty_series_folders": media_mgmt.create_empty_series_folders,
                "delete_empty_folders": media_mgmt.delete_empty_folders,
                "file_date": media_mgmt.file_date,
                "rescan_after_refresh": media_mgmt.rescan_after_refresh,
                "set_permissions_linux": media_mgmt.set_permissions_linux,
                "chmod_folder": media_mgmt.chmod_folder,
                "chown_group": media_mgmt.chown_group,
                "skip_free_space_check_when_importing": media_mgmt.skip_free_space_check_when_importing,
                "minimum_free_space_when_importing": media_mgmt.minimum_free_space_when_importing,
                "copy_using_hardlinks": media_mgmt.copy_using_hardlinks,
                "import_extra_files": media_mgmt.import_extra_files,
                "extra_file_extensions": media_mgmt.extra_file_extensions,
                "enable_media_info": media_mgmt.enable_media_info,
            }
            logger.info("  ✓ Imported media management config")

    # Add instance config to the main config
    config["sonarr_instances"][0].update(instance_config)

    # Write to YAML file
    logger.info(f"Writing configuration to {output_path}...")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, indent=2)

    logger.info("✓ Import complete!")

    if not include_secrets:
        logger.info(
            "\nNote: Secrets have been replaced with environment variable placeholders."
        )
        logger.info("Make sure to set these in your .env file:")
        logger.info(f"  SONARR_MAIN_URL={base_url}")
        logger.info(f"  SONARR_MAIN_API_KEY={api_key}")

    return True


def _serialize_specification(spec) -> dict[str, Any]:
    """Serialize a custom format specification."""
    spec_dict = {
        "name": spec.name,
        "implementation": spec.implementation,
        "negate": spec.negate,
        "required": spec.required,
    }

    if spec.fields:
        spec_dict["fields"] = {field.name: field.value for field in spec.fields}

    return spec_dict


def _serialize_quality_items(items) -> list[dict[str, Any]]:
    """Serialize quality profile items (recursive for groups)."""
    result = []
    for item in items:
        if item.quality:
            # Single quality item
            result.append(
                {
                    "quality": item.quality.name,
                    "allowed": item.allowed,
                }
            )
        elif hasattr(item, "items") and item.items:
            # Quality group
            result.append(
                {
                    "name": item.name,
                    "allowed": item.allowed,
                    "items": _serialize_quality_items(item.items),
                }
            )
    return result


def _serialize_fields(fields, include_secrets: bool) -> dict[str, Any]:
    """
    Serialize indexer/download client fields.

    Args:
        fields: List of field objects
        include_secrets: If False, replace sensitive values with placeholders
    """
    result = {}
    sensitive_names = {"apikey", "api_key", "password", "passkey", "secret", "token"}

    for field in fields:
        value = field.value

        # Check if field is sensitive
        if not include_secrets and field.name.lower() in sensitive_names:
            value = f"${{YOUR_{field.name.upper()}}}"

        result[field.name] = value

    return result
