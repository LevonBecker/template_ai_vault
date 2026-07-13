"""
Update the Ollama binary and all installed models, then prune orphaned blobs.

Usage:
    uv run --no-sync python -m modules.ollama.update
    uv run --no-sync python -m modules.ollama.update --skip-binary
    uv run --no-sync python -m modules.ollama.update --skip-models
    uv run --no-sync python -m modules.ollama.update --skip-cleanup
"""

import json
import shutil
import subprocess
from pathlib import Path

from ..common import cli
from ..common.utils import error, success, warning
from .helpers import pull_model

OLLAMA_MODELS_DIR = Path.home() / ".ollama" / "models"


def update_binary() -> None:
    """Update the Ollama binary via Homebrew."""
    if not shutil.which("brew"):
        error("Homebrew not found.")
    cli.echo("📦 Updating Ollama binary via Homebrew...")
    result = subprocess.run(["brew", "upgrade", "ollama"], check=False)
    if result.returncode != 0:
        warning("Ollama binary upgrade had issues or was already up to date")
    else:
        success("Ollama binary updated")


def get_installed_models() -> list[str]:
    """Return names of all locally installed Ollama models."""
    if not shutil.which("ollama"):
        error("Ollama not found. Run 'invoke ollama.setup' first.")
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        error("Failed to list installed models")
    lines = result.stdout.strip().splitlines()
    return [line.split()[0] for line in lines[1:] if line.split()]


def update_models(models: list[str]) -> None:
    """Pull the latest version of each installed model."""
    for model in models:
        pull_model(model)


def get_referenced_blobs() -> set[str]:
    """Collect all blob filenames referenced across every installed model manifest."""
    manifests_dir = OLLAMA_MODELS_DIR / "manifests"
    referenced: set[str] = set()

    if not manifests_dir.exists():
        return referenced

    for manifest_path in manifests_dir.rglob("*"):
        if not manifest_path.is_file():
            continue
        try:
            data = json.loads(manifest_path.read_text())
        except json.JSONDecodeError, OSError:
            # Skip unreadable manifests — keep their blobs to be safe
            continue

        config_digest = data.get("config", {}).get("digest", "")
        if config_digest:
            referenced.add(config_digest.replace(":", "-"))

        for layer in data.get("layers", []):
            digest = layer.get("digest", "")
            if digest:
                referenced.add(digest.replace(":", "-"))

    return referenced


def cleanup_orphaned_blobs() -> None:
    """Delete blob files in ~/.ollama/models/blobs not referenced by any manifest."""
    blobs_dir = OLLAMA_MODELS_DIR / "blobs"

    if not blobs_dir.exists():
        cli.echo("No Ollama blobs directory found — nothing to clean.")
        return

    referenced = get_referenced_blobs()

    orphaned = [b for b in blobs_dir.iterdir() if b.is_file() and b.name not in referenced]

    if not orphaned:
        success("No orphaned blobs — storage is clean")
        return

    total_bytes = sum(b.stat().st_size for b in orphaned)
    total_gb = total_bytes / (1024**3)
    cli.echo(f"Found {len(orphaned)} orphaned blob(s) ({total_gb:.2f} GB) — removing...")

    for blob in orphaned:
        blob.unlink()

    success(f"Freed {total_gb:.2f} GB of orphaned blobs")


@cli.command()
@cli.option("--skip-binary", is_flag=True, help="Skip Ollama binary update, update models only")
@cli.option("--skip-models", is_flag=True, help="Skip model updates, update binary only")
@cli.option("--skip-cleanup", is_flag=True, help="Skip orphaned blob cleanup")
def main(
    skip_binary: bool = False,
    skip_models: bool = False,
    skip_cleanup: bool = False,
) -> None:
    """Update the Ollama binary and all installed models, then prune orphaned blobs."""
    cli.echo("\n=== Ollama Update ===\n")

    if not skip_binary:
        update_binary()

    if not skip_models:
        cli.echo("\n🔍 Checking installed models...")
        models = get_installed_models()
        if not models:
            cli.echo("No models installed.")
        else:
            cli.echo(f"Found {len(models)} model(s): {', '.join(models)}")
            update_models(models)

    if not skip_cleanup:
        cli.echo("\n🧹 Cleaning up orphaned blobs...")
        cleanup_orphaned_blobs()

    success("Ollama update complete!")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
