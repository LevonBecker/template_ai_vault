"""
Install Ollama and a local coding LLM on Apple Silicon.

Usage:
    uv run --no-sync python -u -m modules.ollama.install --model qwen3:14b
    uv run --no-sync python -u -m modules.ollama.install --model qwen2.5-coder:32b --debug
"""

import platform
import shutil
import subprocess
import sys
import tempfile
import time

from ..common import cli
from ..common.utils import error, success
from .helpers import pull_model, read_char_choice

MODELS: list[tuple[str, str, str, str]] = [
    ("qwen3:14b", "~9GB", "16GB+", "recommended — works best with Cline"),
    ("qwen3:32b", "~20GB", "32GB+", "bigger qwen3 — same family, higher quality"),
    ("qwen2.5-coder:7b", "~5GB", "8GB+", "fastest, lightweight"),
    ("qwen2.5-coder:14b", "~9GB", "16GB+", "good balance"),
    ("qwen2.5-coder:32b", "~20GB", "32GB+", "recommended for 32GB Mac"),
    ("qwen2.5-coder:72b", "~45GB", "64GB+", "best quality for 64GB Mac"),
]

OLLAMA_URL = "http://localhost:11434"

# Ollama defaults num_ctx to ~2K-4K tokens, which an agentic tool like Cline blows
# past within a few tool calls (it then silently truncates/loops instead of erroring).
# We create a larger-context variant tag for agentic use alongside the base model.
# 16K keeps responses fast while still fitting the repo's .clinerules workflow content.
AGENT_NUM_CTX = 16000
AGENT_TAG_SUFFIX = "-16k"


def dbg(message: str, debug: bool) -> None:
    """Print a debug line immediately to stderr."""
    if debug:
        sys.stderr.write(f"[debug] {message}\n")
        sys.stderr.flush()


def check_apple_silicon(debug: bool) -> None:
    """Verify the script is running on Apple Silicon and report total RAM."""
    dbg(">>> check_apple_silicon: start", debug)
    dbg(f"  platform.system()  = {platform.system()!r}", debug)
    dbg(f"  platform.machine() = {platform.machine()!r}", debug)
    if platform.system() != "Darwin" or platform.machine() != "arm64":
        error(f"This script requires Apple Silicon (arm64). Detected: {platform.machine()}")
    success("Apple Silicon confirmed")

    dbg("  running sysctl hw.memsize", debug)
    result = subprocess.run(
        ["sysctl", "-n", "hw.memsize"],
        capture_output=True,
        text=True,
        check=False,
    )
    dbg(f"  sysctl returncode = {result.returncode}", debug)
    dbg(f"  sysctl stdout     = {result.stdout.strip()!r}", debug)
    if result.returncode == 0:
        ram_gb = int(result.stdout.strip()) // (1024**3)
        cli.echo(f"   RAM: {ram_gb}GB")
        dbg(f"  ram_gb = {ram_gb}", debug)
    dbg(">>> check_apple_silicon: done", debug)


def check_homebrew(debug: bool) -> None:
    """Verify Homebrew is installed."""
    dbg(">>> check_homebrew: start", debug)
    brew_path = shutil.which("brew")
    dbg(f"  shutil.which('brew') = {brew_path!r}", debug)
    if not brew_path:
        error("Homebrew not found. Install it first: https://brew.sh")
    success("Homebrew found")
    dbg(">>> check_homebrew: done", debug)


def install_ollama(debug: bool) -> None:
    """Install Ollama via Homebrew if not already present."""
    dbg(">>> install_ollama: start", debug)
    ollama_path = shutil.which("ollama")
    dbg(f"  shutil.which('ollama') = {ollama_path!r}", debug)
    if ollama_path:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True, check=False)
        dbg(f"  ollama --version returncode = {result.returncode}", debug)
        dbg(f"  ollama --version stdout     = {result.stdout.strip()!r}", debug)
        version = result.stdout.strip() if result.returncode == 0 else "version unknown"
        success(f"Ollama already installed ({version})")
        dbg(">>> install_ollama: already installed, done", debug)
        return

    cli.echo("📦 Installing Ollama via Homebrew...")
    result = subprocess.run(["brew", "install", "ollama"], check=False)
    dbg(f"  brew install returncode = {result.returncode}", debug)
    if result.returncode != 0:
        error("Failed to install Ollama via Homebrew")
    success("Ollama installed")
    dbg(">>> install_ollama: done", debug)


def start_ollama_service(debug: bool) -> None:
    """Start the Ollama service and wait until it responds."""
    dbg(">>> start_ollama_service: start", debug)
    cli.echo("🚀 Starting Ollama service...")
    result = subprocess.run(["brew", "services", "start", "ollama"], check=False)
    dbg(f"  brew services start returncode = {result.returncode}", debug)

    cli.echo("   Waiting for Ollama to be ready...")
    for i in range(15):
        dbg(f"  probe {i + 1}/15: curling {OLLAMA_URL}", debug)
        result = subprocess.run(
            ["curl", "-s", OLLAMA_URL],
            capture_output=True,
            check=False,
        )
        dbg(f"  probe {i + 1}/15: returncode = {result.returncode}", debug)
        if result.returncode == 0:
            success(f"Ollama is running at {OLLAMA_URL}")
            dbg(">>> start_ollama_service: done (service up)", debug)
            return
        time.sleep(1)

    error("Ollama did not start in time. Run 'ollama serve' manually and retry.")


def create_agent_variant(model: str, debug: bool) -> str:
    """Create a larger-context tag of `model` for agentic tool use (e.g. Cline). Returns the new tag."""
    agent_tag = f"{model}{AGENT_TAG_SUFFIX}"
    dbg(f">>> create_agent_variant: model={model!r} agent_tag={agent_tag!r}", debug)

    with tempfile.NamedTemporaryFile("w", suffix=".modelfile", delete=False) as fh:
        fh.write(f"FROM {model}\nPARAMETER num_ctx {AGENT_NUM_CTX}\n")
        modelfile_path = fh.name
    dbg(f"  wrote Modelfile to {modelfile_path}", debug)

    result = subprocess.run(
        ["ollama", "create", agent_tag, "-f", modelfile_path],
        capture_output=True,
        text=True,
        check=False,
    )
    dbg(f"  ollama create returncode = {result.returncode}", debug)
    dbg(f"  ollama create stdout     = {result.stdout.strip()!r}", debug)
    dbg(f"  ollama create stderr     = {result.stderr.strip()!r}", debug)

    if result.returncode != 0:
        cli.echo(f"   ⚠️  Could not create {agent_tag} (num_ctx={AGENT_NUM_CTX}): {result.stderr.strip()}")
        return model

    success(f"{agent_tag} ready (num_ctx={AGENT_NUM_CTX}, for use in Cline)")
    dbg(">>> create_agent_variant: done", debug)
    return agent_tag


def select_model_interactive(debug: bool) -> list[str]:
    """Display an interactive numbered menu and return the selected model(s)."""
    dbg(">>> select_model_interactive: start", debug)
    cli.echo("\nSelect a model to install:\n")
    for i, (name, size, ram, desc) in enumerate(MODELS, 1):
        cli.echo(f"  {i}) {name:<26} {size:<7} | {ram:<7} RAM | {desc}")
    extra = len(MODELS) + 1
    cli.echo(f"  {extra}) 32b + 72b              ~65GB  | 64GB+   RAM | full setup")
    cli.echo("")

    dbg(f"  max_choice = {extra}", debug)
    dbg(f"  stdin.isatty() = {sys.stdin.isatty()}", debug)
    dbg("  calling read_char_choice...", debug)
    choice = read_char_choice(extra)
    dbg(f"  read_char_choice returned: {choice}", debug)

    if choice == extra:
        models = ["qwen2.5-coder:32b", "qwen2.5-coder:72b"]
    else:
        models = [MODELS[choice - 1][0]]
    dbg(f"  resolved models: {models}", debug)
    dbg(">>> select_model_interactive: done", debug)
    return models


@cli.command()
@cli.option(
    "--model",
    default=None,
    help="Model to install (e.g. qwen2.5-coder:32b). Omit for interactive menu.",
)
@cli.option("--debug", is_flag=True, help="Print verbose step-by-step debug output")
def main(model: str | None = None, debug: bool = False) -> None:
    """Install Ollama and a local coding LLM on Apple Silicon."""
    dbg(">>> main: entered", debug)
    dbg(f"  model arg = {model!r}", debug)
    dbg(f"  debug arg = {debug!r}", debug)
    dbg(f"  sys.stdout.isatty() = {sys.stdout.isatty()}", debug)
    dbg(f"  sys.stdin.isatty()  = {sys.stdin.isatty()}", debug)
    dbg(f"  sys.version = {sys.version}", debug)

    cli.echo("\n=== Local Coding LLM Setup — Apple Silicon ===\n")

    dbg(">>> calling check_apple_silicon", debug)
    check_apple_silicon(debug)

    dbg(">>> calling check_homebrew", debug)
    check_homebrew(debug)

    dbg(">>> calling install_ollama", debug)
    install_ollama(debug)

    dbg(">>> calling start_ollama_service", debug)
    start_ollama_service(debug)

    dbg(">>> resolving model list", debug)
    if model:
        dbg(f"  using --model flag: {model!r}", debug)
        models = [model]
    else:
        dbg("  no --model flag, using interactive menu", debug)
        models = select_model_interactive(debug)

    dbg(f">>> models to pull: {models}", debug)
    agent_tags: list[str] = []
    for m in models:
        dbg(f">>> calling pull_model({m!r})", debug)
        pull_model(m, debug)
        dbg(f">>> pull_model({m!r}) returned", debug)
        dbg(f">>> calling create_agent_variant({m!r})", debug)
        agent_tags.append(create_agent_variant(m, debug))
        dbg(">>> create_agent_variant returned", debug)

    dbg(">>> calling success", debug)
    success("Setup complete!")

    cli.echo("\n" + "━" * 54)
    cli.echo("Cline setup")
    cli.echo("━" * 54)
    cli.echo("   In Cline's model picker, select the Ollama provider and pick:")
    for tag in agent_tags:
        cli.echo(f"     {tag}")
    cli.echo(f"   (the {AGENT_TAG_SUFFIX} tags have a larger context window — required for")
    cli.echo("    Cline's agent loop; the plain base tags will silently fail")
    cli.echo("    or loop past a few tool calls with Ollama's small default context)")
    cli.echo("   In Cline's Ollama provider settings, set Request Timeout to 120000 ms")
    cli.echo("   (local inference is slower than a hosted API and needs the headroom).")
    cli.echo("   Custom slash commands are available via .clinerules/workflows/")
    cli.echo("   (kept in sync with `inv cline.sync`). Try /push to test.\n")
    dbg(">>> main: done", debug)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
