"""Backup utilities for Sonarr configurations."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from src.utils.logger import get_logger
from src.utils.sonarr_client import SonarrClient

logger = get_logger("backup")


def create_backup(
    client: SonarrClient, backup_dir: Path, instance_name: str
) -> Path | None:
    """
    Create a backup of the current Sonarr configuration.

    Args:
        client: Initialized SonarrClient
        backup_dir: Directory to store backups
        instance_name: Name of the instance being backed up

    Returns:
        Path to the backup file, or None on error
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"{instance_name}_{timestamp}.json"

    logger.info(f"Creating backup: {backup_file}")

    try:
        backup_data: dict[str, Any] = {}

        # Backup all resource types
        logger.debug("Backing up tags...")
        backup_data["tags"] = [
            tag.to_dict() for tag in client.tags.api_v3_tag_get()
        ]

        logger.debug("Backing up custom formats...")
        backup_data["custom_formats"] = [
            cf.to_dict() for cf in client.custom_formats.api_v3_customformat_get()
        ]

        logger.debug("Backing up quality definitions...")
        backup_data["quality_definitions"] = [
            qd.to_dict() for qd in client.quality_definitions.api_v3_qualitydefinition_get()
        ]

        logger.debug("Backing up quality profiles...")
        backup_data["quality_profiles"] = [
            qp.to_dict() for qp in client.quality_profiles.api_v3_qualityprofile_get()
        ]

        logger.debug("Backing up delay profiles...")
        backup_data["delay_profiles"] = [
            dp.to_dict() for dp in client.delay_profiles.api_v3_delayprofile_get()
        ]

        logger.debug("Backing up indexers...")
        backup_data["indexers"] = [
            idx.to_dict() for idx in client.indexers.api_v3_indexer_get()
        ]

        logger.debug("Backing up download clients...")
        backup_data["download_clients"] = [
            dc.to_dict() for dc in client.download_clients.api_v3_downloadclient_get()
        ]

        logger.debug("Backing up naming config...")
        backup_data["naming_config"] = client.naming_config.get_naming_config().to_dict()

        logger.debug("Backing up media management config...")
        backup_data["media_management_config"] = (
            client.media_management_config.api_v3_config_mediamanagement_get().to_dict()
        )

        # Add metadata
        backup_data["_metadata"] = {
            "instance_name": instance_name,
            "timestamp": timestamp,
            "backup_version": "1.0",
        }

        # Write backup
        backup_dir.mkdir(parents=True, exist_ok=True)
        with open(backup_file, "w") as f:
            json.dump(backup_data, f, indent=2, default=str)

        logger.info(f"✓ Backup created: {backup_file}")
        return backup_file

    except Exception as e:
        logger.error(f"Failed to create backup: {e}")
        return None


def list_backups(backup_dir: Path, instance_name: str | None = None) -> list[Path]:
    """
    List available backups.

    Args:
        backup_dir: Directory containing backups
        instance_name: Filter by instance name (optional)

    Returns:
        List of backup file paths, sorted by timestamp (newest first)
    """
    if not backup_dir.exists():
        return []

    pattern = f"{instance_name}_*.json" if instance_name else "*.json"
    backups = sorted(backup_dir.glob(pattern), reverse=True)

    return backups


def cleanup_old_backups(backup_dir: Path, keep_count: int = 5) -> None:
    """
    Remove old backups, keeping only the most recent ones.

    Args:
        backup_dir: Directory containing backups
        keep_count: Number of backups to keep per instance
    """
    if not backup_dir.exists():
        return

    # Group backups by instance name
    instance_backups: dict[str, list[Path]] = {}

    for backup in backup_dir.glob("*.json"):
        # Extract instance name from filename (format: instance_timestamp.json)
        parts = backup.stem.split("_")
        if len(parts) >= 2:
            # Instance name might contain underscores, so join all but last part
            instance = "_".join(parts[:-2]) if len(parts) > 2 else parts[0]
            if instance not in instance_backups:
                instance_backups[instance] = []
            instance_backups[instance].append(backup)

    # Sort and remove old backups for each instance
    for instance, backups in instance_backups.items():
        sorted_backups = sorted(backups, reverse=True)

        if len(sorted_backups) > keep_count:
            for old_backup in sorted_backups[keep_count:]:
                logger.info(f"Removing old backup: {old_backup.name}")
                old_backup.unlink()


def restore_backup(
    client: SonarrClient, backup_file: Path, dry_run: bool = False
) -> bool:
    """
    Restore configuration from a backup file.

    Warning: This will overwrite the current configuration!

    Args:
        client: Initialized SonarrClient
        backup_file: Path to backup file
        dry_run: If True, only show what would be restored

    Returns:
        True on success, False on error
    """
    logger.warning("⚠ Restore functionality is not yet implemented")
    logger.warning(
        "To restore manually, use the import command with the generated YAML file"
    )
    return False
