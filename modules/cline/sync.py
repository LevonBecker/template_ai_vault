"""
Sync Cline workflow files from .github/prompts/*.prompt.md source of truth.

Usage:
    uv run --no-sync python -m modules.cline.sync

NEVER hand-edit .clinerules/workflows/ — run this script instead:
    uv run --no-sync invoke cline.sync
"""

import re
from pathlib import Path

from ..common import cli
from ..common.prompt_commands import load_commands
from ..common.route_utils import find_repo_root

_REPO_ROOT = find_repo_root()
_CLINE_WORKFLOWS_DIR = _REPO_ROOT / ".clinerules" / "workflows"
_EXEC_RE = re.compile(r"^!`(.+)`$")

# "claude.md" collides with Claude Code's own CLAUDE.md auto-loading convention
# on case-insensitive filesystems (APFS) — skip it, same as hermes/sync.py does.
_SKIP_COMMANDS: frozenset[str] = frozenset({"claude"})


def _transform_body(body: str) -> str:
    """Convert Hermes exec lines to plain fenced code blocks Cline can run via its own tools."""
    out_lines: list[str] = []
    for line in body.splitlines():
        m = _EXEC_RE.match(line)
        if m:
            out_lines.extend(["Run this terminal command:", "", "```", m.group(1), "```"])
        else:
            out_lines.append(line)
    return "\n".join(out_lines).strip()


def _workflow_content(body: str) -> str:
    """Return workflow file content for a single command (plain markdown, no frontmatter)."""
    return f"{body}\n" if body else ""


@cli.command()
def main() -> None:
    """Sync .clinerules/workflows/ from .github/prompts/ source of truth."""
    _CLINE_WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)
    cmds = load_commands(skip=_SKIP_COMMANDS)
    for cmd in cmds:
        out: Path = _CLINE_WORKFLOWS_DIR / f"{cmd.slug}.md"
        out.write_text(_workflow_content(_transform_body(cmd.body)), encoding="utf-8")
        cli.echo(f"  ✅ {cmd.slug}.md")
    cli.echo(f"\n✅ Synced {len(cmds)} workflows → .clinerules/workflows/")
    cli.echo("💡 Reload the Cline extension to pick up new workflows.")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
