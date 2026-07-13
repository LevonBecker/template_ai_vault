"""Active chat state management for topic directories."""

import re
from datetime import datetime
from pathlib import Path

import yaml

from ..common import cli as click
from ..common.utils import error

ACTIVE_YML_HEADER = "# Active chat tracker\n# This file is managed by the chat scripts\n# Do not edit manually\n\n"


def _normalize_active_data(data: object) -> dict | None:
    """Return validated active data or None if invalid."""
    if not isinstance(data, dict):
        return None

    filename = data.get("filename")
    title = data.get("title")
    topic = data.get("topic")

    if not isinstance(filename, str) or not filename.strip():
        return None
    if not isinstance(title, str) or not title.strip():
        return None
    if not isinstance(topic, str) or not topic.strip():
        return None

    normalized = dict(data)
    normalized["filename"] = filename.strip()
    normalized["title"] = title.strip()
    normalized["topic"] = topic.strip()

    status = normalized.get("status")
    if not isinstance(status, str) or not status.strip():
        normalized["status"] = "active"
    else:
        normalized["status"] = status.strip()

    return normalized


def create_slug(text: str) -> str:
    """
    Create a URL-safe slug from text.

    Args:
        text: Text to convert to slug.

    Returns:
        Lowercase slug with underscores and hyphens only.
    """
    slug = text.lower().replace(" ", "_")
    slug = "".join(c for c in slug if c.isalnum() or c in ("_", "-"))
    slug = re.sub(r"[_-]+", lambda m: m.group()[0], slug)
    return slug


def read_active(topic_dir: Path) -> dict | None:
    """
    Read active.yml from topic directory.

    Args:
        topic_dir: Path to topic directory.

    Returns:
        Parsed active.yml data, or None if file does not exist.
    """
    active_file = topic_dir / "active.yml"
    if not active_file.exists():
        return None

    try:
        with active_file.open() as f:
            data = yaml.safe_load(f)
            return _normalize_active_data(data)
    except OSError:
        return None
    except yaml.YAMLError:
        return None


def write_active(
    topic_dir: Path,
    filename: str,
    title: str,
    topic_path: str,
    *,
    resumed: bool = False,
) -> None:
    """
    Write active.yml to topic directory.

    Args:
        topic_dir: Path to topic directory.
        filename: Chat filename (e.g. 20260221_my_chat.md).
        title: Human-readable chat title.
        topic_path: Relative topic path (e.g. workshop/tig_welding).
        resumed: If True, uses 'resumed' timestamp key instead of 'started'.
    """
    active_file = topic_dir / "active.yml"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    active_data: dict = {
        "filename": filename,
        "title": title,
        "topic": topic_path,
        "status": "active",
    }

    if resumed:
        active_data["resumed"] = timestamp
    else:
        active_data["started"] = timestamp

    with active_file.open("w") as f:
        f.write(ACTIVE_YML_HEADER)
        yaml.dump(active_data, f, default_flow_style=False)


def clear_active(topic_dir: Path) -> None:
    """
    Remove active.yml from topic directory.

    Args:
        topic_dir: Path to topic directory.

    Raises:
        SystemExit: If file cannot be removed.
    """
    active_file = topic_dir / "active.yml"
    try:
        active_file.unlink()
    except OSError as e:
        error(f"Failed to remove active.yml: {e}")


def abort_if_active(topic_dir: Path) -> None:
    """
    Abort with guidance if an active chat already exists.

    Args:
        topic_dir: Path to topic directory.
    """
    data = read_active(topic_dir)
    if data is None:
        return

    status = str(data.get("status", "")).strip().lower()
    if status and status != "active":
        return

    click.echo("⚠️  Active chat detected:")
    click.echo(f"   File: {data.get('filename')}")
    click.echo(f"   Title: {data.get('title')}")
    click.echo()
    click.echo("You need to close the current chat before resuming another.")
    click.echo("Options:")
    click.echo("  1. Run /chat end to save and commit the current chat")
    click.echo()
    click.echo("After closing, run /chat resume again.")
    raise SystemExit(1)
