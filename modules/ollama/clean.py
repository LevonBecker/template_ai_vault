"""
Remove all downloaded Ollama models and blob cache (~/.ollama/models/).

Usage:
    uv run --no-sync python -m modules.ollama.clean
    uv run --no-sync python -m modules.ollama.clean --yes
"""

import shutil
from pathlib import Path

from ..common import cli
from ..common.utils import success

MODELS_DIR = Path.home() / ".ollama" / "models"


@cli.command()
@cli.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt")
def main(yes: bool = False) -> None:
    """Remove all downloaded Ollama models and blob cache."""
    if not MODELS_DIR.exists():
        cli.echo("Nothing to clean — ~/.ollama/models/ does not exist.")
        return

    size_gb = sum(f.stat().st_size for f in MODELS_DIR.rglob("*") if f.is_file()) / (1024**3)
    cli.echo(f"\nThis will delete ~/.ollama/models/ ({size_gb:.1f}GB)")

    if not yes and not cli.confirm("Are you sure?"):
        cli.echo("Aborted.")
        return

    shutil.rmtree(MODELS_DIR)
    success(f"Removed ~/.ollama/models/ ({size_gb:.1f}GB freed)")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
