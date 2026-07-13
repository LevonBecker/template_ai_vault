"""
List installed and available Ollama models.

Usage:
    uv run --no-sync python -m modules.ollama.list
"""

import shutil
import subprocess

from ..common import cli
from ..common.utils import error
from .install import MODELS


def get_installed() -> list[tuple[str, str]]:
    """Return (name, size) for each locally installed Ollama model."""
    if not shutil.which("ollama"):
        error("Ollama not found. Run 'invoke ollama.install' first.")
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        error("Failed to list installed models")

    installed: list[tuple[str, str]] = []
    for line in result.stdout.strip().splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 4:
            installed.append((parts[0], f"{parts[2]} {parts[3]}"))
    return installed


@cli.command()
def main() -> None:
    """List installed and available Ollama models."""
    cli.echo("\n=== Installed Ollama Models ===\n")
    installed = get_installed()
    if not installed:
        cli.echo("  (none installed)")
    else:
        for name, size in installed:
            cli.echo(f"  ✅ {name:<26} {size}")

    installed_names = {name for name, _ in installed}

    cli.echo("\n=== Available to Install ===\n")
    for name, size, ram, desc in MODELS:
        status = "✅ installed" if name in installed_names else f"{size:<7} | {ram:<7} RAM"
        cli.echo(f"  {name:<26} {status:<20} | {desc}")

    cli.echo("\n💡 Install one with: uv run --no-sync invoke ollama.install --model <name>\n")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
