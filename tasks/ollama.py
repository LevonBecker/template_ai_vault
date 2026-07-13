"""Ollama tasks for local LLM setup and maintenance."""

import shutil
from pathlib import Path

from invoke import task


@task
def clean(_context, yes=False):
    """Remove all downloaded Ollama models and blob cache (~/.ollama/models/)

    Args:
        yes: Skip confirmation prompt
    """
    models_dir = Path.home() / ".ollama" / "models"
    if not models_dir.exists():
        print("Nothing to clean — ~/.ollama/models/ does not exist.")
        return

    size_gb = sum(f.stat().st_size for f in models_dir.rglob("*") if f.is_file()) / (1024**3)
    print(f"\nThis will delete ~/.ollama/models/ ({size_gb:.1f}GB)")

    if not yes:
        confirm = input("Are you sure? [y/N]: ").strip().lower()
        if confirm != "y":
            print("Aborted.")
            return

    shutil.rmtree(models_dir)
    print(f"✅ Removed ~/.ollama/models/ ({size_gb:.1f}GB freed)")


@task
def install(context, model="qwen2.5-coder:32b", debug=False):
    """Install Ollama and a local coding LLM on Apple Silicon

    Args:
        model: Model to install (default: qwen2.5-coder:32b)
        debug: Enable verbose step-by-step debug logging
    """
    title = "Ollama Install (Debug Mode)" if debug else "Ollama Install"
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50 + "\n")
    debug_flag = "--debug" if debug else ""
    context.run(f"python -u -m modules.ollama.install --model {model} {debug_flag}")


@task(name="list")
def list_models(context):
    """List installed and available Ollama models"""
    context.run("python -m modules.ollama.list")


@task
def restart(context):
    """Restart the Ollama service via Homebrew"""
    context.run("brew services restart ollama")


@task
def start(context):
    """Start the Ollama service via Homebrew"""
    context.run("brew services start ollama")


@task
def status(context):
    """Show Ollama service and running-model status"""
    context.run("python -m modules.ollama.status")


@task
def stop(context):
    """Stop the Ollama service via Homebrew"""
    context.run("brew services stop ollama")


@task
def uninstall(context):
    """Uninstall Ollama binary and remove all downloaded models"""
    print("\n" + "=" * 50)
    print("Ollama Uninstall")
    print("=" * 50 + "\n")
    context.run("python -u -m modules.ollama.uninstall")


@task
def update(context, debug=False):
    """Update Ollama binary and all installed models

    Args:
        debug: Enable verbose step-by-step debug logging
    """
    title = "Ollama Update (Debug Mode)" if debug else "Ollama Update"
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50 + "\n")
    debug_flag = "--debug" if debug else ""
    context.run(f"python -u -m modules.ollama.update {debug_flag}")
