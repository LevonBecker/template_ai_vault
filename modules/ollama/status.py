"""
Show Ollama service and running-model status.

Usage:
    uv run --no-sync python -m modules.ollama.status
"""

import shutil
import subprocess
import urllib.error
import urllib.request

from ..common import cli
from ..common.utils import success, warning

OLLAMA_URL = "http://localhost:11434"


def check_binary() -> str | None:
    """Return the installed Ollama version string, or None if not installed."""
    if not shutil.which("ollama"):
        return None
    result = subprocess.run(["ollama", "--version"], capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else "version unknown"


def check_service() -> bool:
    """Return True if the Ollama service is responding."""
    try:
        with urllib.request.urlopen(OLLAMA_URL, timeout=3):
            return True
    except urllib.error.URLError:
        return False


def print_loaded_models() -> None:
    """Print currently loaded (in-memory) models via `ollama ps`."""
    result = subprocess.run(["ollama", "ps"], capture_output=True, text=True, check=False)
    lines = result.stdout.strip().splitlines()
    if len(lines) <= 1:
        cli.echo("  (no models currently loaded in memory)")
        return
    for line in lines:
        cli.echo(f"  {line}")


@cli.command()
def main() -> None:
    """Show Ollama service and running-model status."""
    cli.echo("\n=== Ollama Service Status ===\n")

    version = check_binary()
    if version is None:
        warning("Ollama not installed. Run 'inv ollama.install' first.")
        return
    success(f"Ollama installed ({version})")

    if check_service():
        success(f"Service running at {OLLAMA_URL}")
    else:
        warning(f"Service not responding at {OLLAMA_URL}. Run 'inv ollama.start'.")
        return

    cli.echo("\n=== Loaded Models (in memory) ===\n")
    print_loaded_models()
    cli.echo("")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
