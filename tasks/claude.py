"""Claude Code integration tasks."""

from invoke import task


@task
def sync(context, force=False):
    """Sync .claude/commands/ from .github/prompts/ source of truth."""
    flag = " --force" if force else ""
    context.run(f"uv run --no-sync python -m modules.claude.sync{flag}", pty=True)
