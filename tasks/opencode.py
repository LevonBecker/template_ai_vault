"""OpenCode integration tasks."""

from invoke import task


@task
def sync(context, force=False):
    """Sync .opencode/command/ from .github/prompts/ source of truth."""
    flag = " --force" if force else ""
    context.run(f"uv run --no-sync python -m modules.opencode.sync{flag}", pty=True)
