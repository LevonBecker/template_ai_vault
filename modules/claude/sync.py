"""
Sync Claude Code slash commands from .github/prompts/*.prompt.md source of truth.

By default only writes NEW commands (files that don't exist yet).
Use --force to overwrite existing hand-crafted command files.

Usage:
    uv run --no-sync python -m modules.claude.sync          # additive only
    uv run --no-sync python -m modules.claude.sync --force  # overwrite all
    uv run --no-sync invoke claude.sync
    uv run --no-sync invoke claude.sync --force
"""

from pathlib import Path

from ..common import cli
from ..common.prompt_commands import load_commands
from ..common.route_utils import find_repo_root

_REPO_ROOT = find_repo_root()
_CLAUDE_COMMANDS_DIR = _REPO_ROOT / ".claude" / "commands"

# A /claude command inside Claude Code itself would just proxy back to the running tool — skip it.
_SKIP_COMMANDS: frozenset[str] = frozenset({"claude"})


def _command_content(description: str, body: str) -> str:
    header = f"---\ndescription: {description}\n---"
    return f"{header}\n\n{body}\n" if body else f"{header}\n"


@cli.option("--force", is_flag=True, default=False, help="Overwrite existing command files")
@cli.command()
def main(force: bool = False) -> None:
    """Sync .claude/commands/ from .github/prompts/ source of truth."""
    _CLAUDE_COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
    cmds = load_commands(skip=_SKIP_COMMANDS)
    written = skipped = 0
    for cmd in cmds:
        out: Path = _CLAUDE_COMMANDS_DIR / f"{cmd.slug}.md"
        if out.exists() and not force:
            cli.echo(f"  ⏭️  {cmd.slug}.md (exists — use --force to overwrite)")
            skipped += 1
        else:
            out.write_text(_command_content(cmd.description, cmd.body), encoding="utf-8")
            cli.echo(f"  ✅ {cmd.slug}.md")
            written += 1
    cli.echo(f"\n✅ Synced {written} new commands → .claude/commands/ ({skipped} skipped)")
    if written:
        cli.echo("💡 Restart Claude Code to pick up new commands.")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
