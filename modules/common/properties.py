"""Properties management for AI Vault repository."""

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


def _expand_path(value: str) -> Path:
    """Expand ~ and environment variables (e.g. $HOME) in a properties.yml path value."""
    return Path(os.path.expandvars(os.path.expanduser(value)))


@lru_cache(maxsize=1)
def get_repo_root() -> Path:
    """
    Find repository root by searching upward for properties.yml.

    Works from any subdirectory within the repository.

    Returns:
        Path to repository root.

    Raises:
        FileNotFoundError: If properties.yml cannot be found.
    """
    # Start from current file location
    current = Path(__file__).resolve()

    # Search upward from current file location
    for parent in [current.parent.parent.parent] + list(current.parents):
        props_file = parent / "properties.yml"
        if props_file.exists():
            return parent

    # Also try from current working directory
    current_cwd = Path.cwd().resolve()
    for parent in [current_cwd] + list(current_cwd.parents):
        props_file = parent / "properties.yml"
        if props_file.exists():
            return parent

    msg = (
        "properties.yml not found. This repo needs a machine-specific properties.yml "
        "(gitignored) — run `uv run --no-sync invoke setup.properties` to create and "
        "configure it, then try again."
    )
    raise FileNotFoundError(msg)


@lru_cache(maxsize=1)
def get_properties() -> dict[str, Any]:
    """
    Load properties.yml with singleton pattern (cached).

    Returns:
        Dictionary with all repository properties.

    Raises:
        FileNotFoundError: If properties.yml does not exist.
    """
    repo_root = get_repo_root()
    props_file = repo_root / "properties.yml"

    with props_file.open() as f:
        return yaml.safe_load(f)


def get_repo_local() -> Path:
    """
    Get repo local path as Path object.

    Returns:
        Path to local repository.
    """
    props = get_properties()
    return _expand_path(props["repo"]["local"])


def get_repo_remote() -> str:
    """
    Get repo remote URL.

    Returns:
        Remote repository URL.
    """
    props = get_properties()
    return props["repo"]["remote"]


def get_skeleton_local() -> Path:
    """
    Get the local path to the shared skeleton repo (template_python), used by /sync-setup.

    A relative path is resolved against this repo's root.

    Returns:
        Path to the skeleton repository.
    """
    props = get_properties()
    local = _expand_path(props["skeleton"]["local"])
    return local if local.is_absolute() else get_repo_root() / local


def get_skeleton_remote() -> str:
    """
    Get the skeleton repo's remote (e.g. "github.com/LevonBecker/template_python").

    Returns:
        Remote repository reference, without a URL scheme.
    """
    props = get_properties()
    return props["skeleton"]["remote"]


def get_icloud_path() -> Path:
    """
    Get iCloud sync path as Path object.

    Returns:
        Path to iCloud sync location.
    """
    props = get_properties()
    return _expand_path(props["icloud"]["path"])


def get_screenshots_location() -> Path:
    """
    Get screenshots directory path as Path object.

    Returns:
        Path to screenshots directory.
    """
    props = get_properties()
    return _expand_path(props["screenshots"]["location"])


def get_screenshots_latest_file() -> str:
    """
    Get latest screenshot filename.

    Returns:
        Filename for latest screenshot.
    """
    props = get_properties()
    return props["screenshots"]["latest_file"]


def get_screenshots_preserve_files() -> list[str]:
    """
    Get list of screenshot files to preserve during cleanup.

    Returns:
        List of filenames to preserve.
    """
    props = get_properties()
    return props["screenshots"]["preserve_files"]


def get_screenshots_cleanup_patterns() -> list[str]:
    """
    Get list of file patterns to clean up.

    Returns:
        List of glob patterns for cleanup.
    """
    props = get_properties()
    return props["screenshots"]["cleanup_patterns"]
