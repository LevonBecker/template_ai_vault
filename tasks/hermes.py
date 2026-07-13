"""Hermes AI agent integration tasks."""

from invoke import task


@task
def sync(context):
    """Sync Hermes /r-* commands from .github/prompts source of truth."""
    context.run("uv run --no-sync python -m modules.hermes.sync", pty=True)
    print("\n💡 Restart your Hermes session (/quit then hermes) to pick up new commands.")
