"""Generic reconciliation engine for syncing resources."""

from typing import Any, Callable, Generic, Optional, TypeVar

from src.core.diff import ChangeSet, compute_diff
from src.shared.mappers.base import ResourceMapper
from src.utils.logger import get_logger

TApiModel = TypeVar("TApiModel")
TYamlDef = TypeVar("TYamlDef")

logger = get_logger("reconciler")


class Reconciler(Generic[TApiModel, TYamlDef]):
    """
    Generic reconciler for syncing a resource type between YAML config and server.

    Handles:
    - Fetching current state from server
    - Computing diff with desired state
    - Applying changes (create/update/delete)
    - Dry-run mode
    """

    def __init__(
        self,
        resource_name: str,
        mapper: ResourceMapper[TApiModel, TYamlDef],
        list_fn: Callable[[], list[TApiModel]],
        create_fn: Callable[[TApiModel], TApiModel],
        update_fn: Callable[[int, TApiModel], TApiModel],
        delete_fn: Callable[[int], None],
    ):
        """
        Initialize the reconciler.

        Args:
            resource_name: Human-readable name (e.g., "Custom Format")
            mapper: ResourceMapper instance
            list_fn: Function to fetch all resources from server
            create_fn: Function to create a resource
            update_fn: Function to update a resource (takes ID + model)
            delete_fn: Function to delete a resource by ID
        """
        self.resource_name = resource_name
        self.mapper = mapper
        self.list_fn = list_fn
        self.create_fn = create_fn
        self.update_fn = update_fn
        self.delete_fn = delete_fn

    def reconcile(
        self,
        desired: list[TYamlDef],
        delete_unmanaged: bool = False,
        dry_run: bool = False,
        context: Optional[dict[str, Any]] = None,
    ) -> ChangeSet:
        """
        Reconcile desired state with current server state.

        Args:
            desired: List of desired resources from YAML
            delete_unmanaged: Whether to delete unmanaged resources
            dry_run: If True, only compute changes without applying
            context: Additional context for mapper (e.g., tag ID lookups)

        Returns:
            ChangeSet of applied/planned changes
        """
        context = context or {}

        logger.info(f"Reconciling {self.resource_name}...")

        # Fetch current state
        current_models = self.list_fn()
        current = [self.mapper.from_api_model(model) for model in current_models]

        logger.debug(f"Found {len(current)} existing {self.resource_name}(s) on server")
        logger.debug(f"Desired state has {len(desired)} {self.resource_name}(s)")

        # Convert desired YAML defs to comparable dicts
        desired_dicts = []
        for yaml_def in desired:
            # We need to convert to dict for comparison
            # But we keep the original yaml_def for creating API models
            api_model = self.mapper.to_api_model(yaml_def, **context)
            desired_dict = self.mapper.from_api_model(api_model)
            desired_dict["_yaml_def"] = yaml_def  # Attach for later use
            desired_dicts.append(desired_dict)

        # Compute diff
        changeset = compute_diff(
            current=current,
            desired=desired_dicts,
            match_key_fn=self.mapper.get_match_key,
            needs_update_fn=lambda cur, des: self.mapper.needs_update(cur, des),
            delete_unmanaged=delete_unmanaged,
        )

        # Log summary
        if changeset:
            logger.info(f"{self.resource_name}: {changeset.summary()}")
        else:
            logger.info(f"{self.resource_name}: no changes needed")

        if dry_run:
            self._log_dry_run_changes(changeset)
            return changeset

        # Apply changes
        self._apply_changes(changeset, context)

        return changeset

    def _apply_changes(self, changeset: ChangeSet, context: dict[str, Any]) -> None:
        """Apply the computed changes to the server."""
        errors = []

        # Create new resources
        for desired_dict in changeset.to_create:
            yaml_def = desired_dict.pop("_yaml_def")
            name = self.mapper.get_match_key(desired_dict)
            logger.info(f"Creating {self.resource_name}: {name}")
            try:
                api_model = self.mapper.to_api_model(yaml_def, **context)
                self.create_fn(api_model)
                logger.info(f"✓ Created {self.resource_name}: {name}")
            except Exception as e:
                error_msg = self._format_api_error(e)
                logger.error(f"✗ Failed to create {self.resource_name} '{name}': {error_msg}")
                errors.append(f"Create {name}: {error_msg}")

        # Update existing resources
        for current_dict, desired_dict in changeset.to_update:
            yaml_def = desired_dict.pop("_yaml_def")
            name = self.mapper.get_match_key(desired_dict)
            resource_id = current_dict["id"]
            logger.info(f"Updating {self.resource_name}: {name} (ID: {resource_id})")
            try:
                api_model = self.mapper.to_api_model(yaml_def, **context)
                # Preserve the ID for update
                api_model.id = resource_id
                self.update_fn(resource_id, api_model)
                logger.info(f"✓ Updated {self.resource_name}: {name}")
            except Exception as e:
                error_msg = self._format_api_error(e)
                logger.error(f"✗ Failed to update {self.resource_name} '{name}': {error_msg}")
                errors.append(f"Update {name}: {error_msg}")

        # Delete unmanaged resources
        for current_dict in changeset.to_delete:
            name = self.mapper.get_match_key(current_dict)
            resource_id = current_dict["id"]
            logger.info(f"Deleting {self.resource_name}: {name} (ID: {resource_id})")
            try:
                self.delete_fn(resource_id)
                logger.info(f"✓ Deleted {self.resource_name}: {name}")
            except Exception as e:
                error_msg = self._format_api_error(e)
                logger.error(f"✗ Failed to delete {self.resource_name} '{name}': {error_msg}")
                errors.append(f"Delete {name}: {error_msg}")

        # Report summary if there were errors
        if errors:
            logger.warning(
                f"Completed with {len(errors)} error(s) for {self.resource_name}"
            )
            
    def _format_api_error(self, exception: Exception) -> str:
        """
        Format API exceptions into readable error messages.
        
        Args:
            exception: The exception to format
            
        Returns:
            Formatted error message string
        """
        error_str = str(exception)
        
        # Try to extract meaningful error from API responses
        if hasattr(exception, 'body'):
            try:
                import json
                body = json.loads(exception.body) if isinstance(exception.body, str) else exception.body
                if isinstance(body, dict) and 'message' in body:
                    return body['message']
                return str(body)
            except (json.JSONDecodeError, AttributeError):
                pass
        
        # Try to extract from response attribute
        if hasattr(exception, 'response'):
            try:
                response = exception.response
                if hasattr(response, 'text'):
                    return response.text[:200]  # Limit length
            except AttributeError:
                pass
        
        # Check for common connection errors
        if 'Connection refused' in error_str:
            return "Connection refused - is the server running?"
        if 'timeout' in error_str.lower():
            return "Request timeout - server not responding"
        if 'Unauthorized' in error_str or '401' in error_str:
            return "Authentication failed - check your API key"
        if 'Not Found' in error_str or '404' in error_str:
            return "Resource not found - API endpoint may not exist"
        
        # Return cleaned up error string
        return error_str[:200]  # Limit to 200 chars

    def _log_dry_run_changes(self, changeset: ChangeSet) -> None:
        """Log planned changes in dry-run mode."""
        logger.info(f"[DRY RUN] Changes for {self.resource_name}:")

        if not changeset:
            logger.info("  No changes needed")
            return

        if changeset.to_create:
            logger.info(f"  Would create {len(changeset.to_create)} item(s):")
            for desired_dict in changeset.to_create:
                name = self.mapper.get_match_key(desired_dict)
                logger.info(f"    + {name}")

        if changeset.to_update:
            logger.info(f"  Would update {len(changeset.to_update)} item(s):")
            for current_dict, desired_dict in changeset.to_update:
                name = self.mapper.get_match_key(desired_dict)
                logger.info(f"    ~ {name}")

        if changeset.to_delete:
            logger.info(f"  Would delete {len(changeset.to_delete)} item(s):")
            for current_dict in changeset.to_delete:
                name = self.mapper.get_match_key(current_dict)
                logger.info(f"    - {name}")
