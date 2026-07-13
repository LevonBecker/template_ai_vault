"""Cline integration tasks."""

from invoke import task


@task
def sync(context):
    """Sync .clinerules/workflows/ from .github/prompts/ source of truth."""
    context.run("uv run --no-sync python -m modules.cline.sync", pty=True)
