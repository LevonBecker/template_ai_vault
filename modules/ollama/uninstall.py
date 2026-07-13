"""
Uninstall Ollama — stops the service, removes models, and uninstalls the binary.

Usage:
    uv run --no-sync python -m modules.ollama.uninstall
    uv run --no-sync python -m modules.ollama.uninstall --yes
    uv run --no-sync python -m modules.ollama.uninstall --keep-models
"""

import shutil
import subprocess
from pathlib import Path

from ..common import cli
from ..common.utils import error, success, warning

OLLAMA_DIR = Path.home() / ".ollama"


def stop_service() -> None:
    """Stop the Ollama brew service if running."""
    if not shutil.which("brew"):
        return
    cli.echo("🛑 Stopping Ollama service...")
    subprocess.run(["brew", "services", "stop", "ollama"], check=False)
    success("Ollama service stopped")


def remove_models_dir() -> None:
    """Delete ~/.ollama and all downloaded models and blobs."""
    if not OLLAMA_DIR.exists():
        cli.echo("No ~/.ollama directory found — nothing to remove.")
        return

    size_bytes = sum(f.stat().st_size for f in OLLAMA_DIR.rglob("*") if f.is_file())
    size_gb = size_bytes / (1024**3)
    cli.echo(f"🗑️  Removing ~/.ollama ({size_gb:.2f} GB)...")
    shutil.rmtree(OLLAMA_DIR)
    success(f"Removed ~/.ollama — freed {size_gb:.2f} GB")


def uninstall_binary() -> None:
    """Uninstall the Ollama binary via Homebrew."""
    if not shutil.which("brew"):
        error("Homebrew not found.")
    if not shutil.which("ollama"):
        cli.echo("Ollama binary not found — already uninstalled.")
        return
    cli.echo("📦 Uninstalling Ollama via Homebrew...")
    result = subprocess.run(["brew", "uninstall", "ollama"], check=False)
    if result.returncode != 0:
        warning("Homebrew uninstall had issues")
    else:
        success("Ollama binary removed")


@cli.command()
@cli.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt")
@cli.option("--keep-models", is_flag=True, help="Remove binary only, keep downloaded models")
def main(yes: bool = False, keep_models: bool = False) -> None:
    """Uninstall Ollama — stops the service, removes models, and uninstalls the binary."""
    cli.echo("\n=== Ollama Uninstall ===\n")

    if keep_models:
        cli.echo("Will remove: Ollama binary")
        cli.echo("Will keep:   Downloaded models (~/.ollama)\n")
    else:
        size_bytes = sum(f.stat().st_size for f in OLLAMA_DIR.rglob("*") if f.is_file()) if OLLAMA_DIR.exists() else 0
        size_gb = size_bytes / (1024**3)
        cli.echo("Will remove: Ollama binary + all downloaded models")
        cli.echo(f"             ~/.ollama ({size_gb:.2f} GB will be freed)\n")

    if not yes and not cli.confirm("⚠️  Proceed with uninstall?"):
        cli.echo("Cancelled.")
        raise SystemExit(0)

    cli.echo("")
    stop_service()

    if not keep_models:
        remove_models_dir()

    uninstall_binary()

    success("Ollama uninstall complete!")
    if keep_models:
        cli.echo(f"\n💡 Models are still in {OLLAMA_DIR} — delete manually if needed.")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
