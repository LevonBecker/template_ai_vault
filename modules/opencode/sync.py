"""
Sync OpenCode slash commands from .github/prompts/*.prompt.md source of truth.

By default only writes NEW commands (files that don't exist yet).
Use --force to overwrite existing hand-crafted command files.

Usage:
    uv run --no-sync python -m modules.opencode.sync          # additive only
    uv run --no-sync python -m modules.opencode.sync --force  # overwrite all
    uv run --no-sync invoke opencode.sync
    uv run --no-sync invoke opencode.sync --force
"""

from pathlib import Path

from ..common import cli
from ..common.prompt_commands import load_commands
from ..common.route_utils import find_repo_root

_REPO_ROOT = find_repo_root()
_OPENCODE_COMMAND_DIR = _REPO_ROOT / ".opencode" / "command"


def _command_content(slug: str, description: str, body: str) -> str:
    header = f"---\ndescription: {description}\nsubtask: false\nagent: general\nslash_command: /{slug}\n---"
    return f"{header}\n\n{body}\n" if body else f"{header}\n"


@cli.option("--force", is_flag=True, default=False, help="Overwrite existing command files")
@cli.command()
def main(force: bool = False) -> None:
    """Sync .opencode/command/ from .github/prompts/ source of truth."""
    _OPENCODE_COMMAND_DIR.mkdir(parents=True, exist_ok=True)
    # Unlike Claude Code and Cline, /claude is legitimate here — it proxies to the real `claude`
    # CLI from within OpenCode, so nothing is skipped.
    cmds = load_commands()
    written = skipped = 0
    for cmd in cmds:
        out: Path = _OPENCODE_COMMAND_DIR / f"{cmd.slug}.md"
        if out.exists() and not force:
            cli.echo(f"  ⏭️  {cmd.slug}.md (exists — use --force to overwrite)")
            skipped += 1
        else:
            out.write_text(_command_content(cmd.slug, cmd.description, cmd.body), encoding="utf-8")
            cli.echo(f"  ✅ {cmd.slug}.md")
            written += 1
    cli.echo(f"\n✅ Synced {written} new commands → .opencode/command/ ({skipped} skipped)")
    if written:
        cli.echo("💡 Restart OpenCode to pick up new commands.")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
