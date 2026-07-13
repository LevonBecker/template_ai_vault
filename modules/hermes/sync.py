"""Sync Hermes /r-* commands from .github/prompts/*.prompt.md source of truth.

This script reads all .github/prompts/*.prompt.md files (the canonical source of
truth for all slash commands in this repo), classifies each command, and writes:

  1. The quick_commands block in ~/.hermes/config.yaml  (exec-style, zero-token)
  2. A complete r-research SKILL.md in ~/.hermes/skills/r-research/SKILL.md
     (routing table for AI-routed and AI-guided commands)

NEVER hand-edit those two output files — run this script instead:
  uv run --no-sync invoke hermes.sync

WARNING: This script owns the entire quick_commands key in config.yaml.
If you manually add non-r- quick_commands, they will be overwritten on the
next sync run. If mixed quick_commands are ever needed, update this script
to merge instead of replace.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from modules.common.route_utils import find_repo_root

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = find_repo_root()
PROMPTS_DIR = REPO_ROOT / ".github" / "prompts"
HERMES_CONFIG = Path.home() / ".hermes" / "config.yaml"
HERMES_SKILL_DIR = Path.home() / ".hermes" / "skills" / "r-research"
HERMES_SKILL_FILE = HERMES_SKILL_DIR / "SKILL.md"

# Commands that are exec-style but too long-running for the 30 s quick_commands timeout
LONG_RUNNING: frozenset[str] = frozenset({"test", "upgrade"})

# Commands to skip entirely — not useful as Hermes /r-* commands
SKIP_COMMANDS: frozenset[str] = frozenset({"claude"})

# Shell command overrides for specific prompts.
# Key = prompt name (underscored), value = full shell command (use {repo_root} placeholder).
EXEC_OVERRIDES: dict[str, str] = {
    "fix": "cd {repo_root} && uv run --no-sync invoke fix",
    "test": "cd {repo_root} && uv run --no-sync invoke test",
    "upgrade": "cd {repo_root} && uv run --no-sync invoke upgrade.upgrade",
}


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


class PromptCommand:  # pylint: disable=too-many-instance-attributes
    """Parsed representation of one .github/prompts/*.prompt.md file."""

    def __init__(self, path: Path) -> None:
        self.path = path
        # name uses underscores (Python identifier), slug preserves hyphens (for r- prefix)
        self.slug: str = path.stem.replace(".prompt", "")
        self.name: str = self.slug.replace("-", "_")
        self.description: str = ""
        self.argument_hint: str = ""
        self.exec_line: str = ""
        self.body: str = ""
        self.classification: str = ""
        self._parse()

    def _parse(self) -> None:
        text = self.path.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            self.body = parts[2].strip()
            try:
                fm: dict = yaml.safe_load(fm_text) or {}
            except yaml.YAMLError:
                fm = {}
            self.description = str(fm.get("description", ""))
            self.argument_hint = str(fm.get("argument-hint", ""))
        else:
            self.body = text.strip()

        # Find exec line: line starting with !`
        exec_match = re.search(r"^!`([^`]+)`", self.body, re.MULTILINE)
        if exec_match:
            self.exec_line = exec_match.group(1).strip()

        # Classify
        if self.name in LONG_RUNNING and self.exec_line:
            self.classification = "exec_long"
        elif not self.exec_line:
            self.classification = "ai_guided"
        elif "$ARGUMENTS" in self.exec_line:
            self.classification = "arg"
        else:
            self.classification = "exec"

    @property
    def r_name(self) -> str:
        """The Hermes /r- command name (e.g. r-pull, r-add-expense)."""
        return f"r-{self.slug}"

    def shell_command(self) -> str:
        """Return the shell command for quick_commands (exec classification only)."""
        repo = str(REPO_ROOT)
        if self.name in EXEC_OVERRIDES:
            return EXEC_OVERRIDES[self.name].format(repo_root=repo)
        cmd = self.exec_line
        if cmd.startswith("uv run"):
            cmd = f"cd {repo} && {cmd}"
        return cmd


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


def load_commands() -> list[PromptCommand]:
    """Load and parse all .github/prompts/*.prompt.md files, deduplicating by name."""
    files = sorted(PROMPTS_DIR.glob("*.prompt.md"))
    seen: set[str] = set()
    unique: list[PromptCommand] = []
    for path in files:
        cmd = PromptCommand(path)
        if cmd.name in SKIP_COMMANDS:
            continue
        if cmd.name in seen:
            # Warn only if descriptions differ — could indicate accidental divergence
            existing = next(c for c in unique if c.name == cmd.name)
            if existing.description != cmd.description:
                print(
                    f"  ⚠️  Duplicate '{cmd.name}' with differing descriptions "
                    f"({cmd.slug!r} vs {existing.slug!r}) — keeping {existing.slug!r}",
                    file=sys.stderr,
                )
            continue
        seen.add(cmd.name)
        unique.append(cmd)
    return unique


# ---------------------------------------------------------------------------
# Generator: quick_commands dict
# ---------------------------------------------------------------------------


def generate_quick_commands(cmds: list[PromptCommand]) -> dict:
    """Return dict for config.yaml quick_commands (exec-style, zero-token only).

    Only "exec" classified commands are wired here. Commands classified as
    arg, exec_long, or ai_guided require AI reasoning and are instead routed
    via the r-research SKILL.md (see generate_skill_md).
    """
    result: dict = {}
    for cmd in cmds:
        if cmd.classification == "exec":
            result[cmd.r_name] = {"type": "exec", "command": cmd.shell_command()}
    return result


# ---------------------------------------------------------------------------
# Generator: SKILL.md
# ---------------------------------------------------------------------------

_SKILL_HEADER_TEMPLATE = """\
---
name: r-research
description: "Research repo (/r-* commands): routing table for topic, chat,\
 repo, and all other template_ai_vault slash commands.\
 AUTO-GENERATED by modules/hermes/sync.py — do not hand-edit."
version: 1.0.0
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [research, routing, slash-commands]
---

# Research Repo — `/r-*` Command System

> **AUTO-GENERATED** by `modules/hermes/sync.py`.
> Re-run `uv run --no-sync invoke hermes.sync` after adding or modifying
> any `.github/prompts/*.prompt.md` file. Never hand-edit this file.

This skill is the routing table for the research repo at:
`{repo_root}`

The repo covers your full range of AI-assisted research topics —
home, health, shopping, travel, finances — organized by topic.

## Critical Conventions

- **ALWAYS `--no-sync`:** `uv run --no-sync python -m ...` — never omit
- **Repo root:** `{repo_root}`
- **Architecture:** Prompt files → `modules/*/route.py` router → `modules/*/*.py` logic
- **Tests:** `uv run --no-sync invoke test` must pass 10/10 before committing `.py`/`.yml`

"""


def _build_exec_section(cmds: list[PromptCommand]) -> str:
    """Build the zero-token quick commands table section."""
    exec_cmds = [c for c in cmds if c.classification == "exec"]
    if not exec_cmds:
        return ""
    rows = "\n".join(f"| `/{c.r_name}` | {c.description} |" for c in exec_cmds)
    return (
        "## Zero-Token Quick Commands (wired in `~/.hermes/config.yaml`)\n\n"
        "These run via `quick_commands` — no LLM call, instant execution:\n\n"
        "| Command | Description |\n"
        "|---|---|\n"
        f"{rows}\n\n"
    )


def _build_exec_long_section(cmds: list[PromptCommand]) -> str:
    """Build the long-running exec section."""
    long_cmds = [c for c in cmds if c.classification == "exec_long"]
    if not long_cmds:
        return ""
    rows = "\n".join(f"| `/{c.r_name}` | `{c.shell_command()}` |" for c in long_cmds)
    return (
        "## Long-Running Exec Commands (use terminal tool)\n\n"
        "These are exec-style but exceed the 30 s `quick_commands` timeout.\n"
        "Ask Hermes to run them via `terminal(background=True, notify_on_complete=True)`:\n\n"
        "| Command | Shell command |\n"
        "|---|---|\n"
        f"{rows}\n\n"
    )


def _body_extra(cmd: PromptCommand) -> str:
    """Return body text after the !` exec line (AI guidance notes)."""
    lines = cmd.body.split("\n")
    past_exec = False
    after: list[str] = []
    for line in lines:
        if line.startswith("!`") and not past_exec:
            past_exec = True
            continue
        if past_exec:
            after.append(line)
    return "\n".join(after).strip()


def _build_arg_section(cmds: list[PromptCommand], repo_root: str) -> str:
    """Build the AI-routed commands section (one subsection per command)."""
    arg_cmds = [c for c in cmds if c.classification == "arg"]
    if not arg_cmds:
        return ""
    parts = [
        "## AI-Routed Commands (Hermes executes via terminal tool)\n\n"
        "For these, run the appropriate `uv run --no-sync` command based on the arguments.\n\n"
        "> **Note:** These are wired as `type: alias` quick_commands pointing to `/r-research`.\n"
        "> When invoked as `/r-<cmd> <args>`, Hermes sees `r-<cmd> <args>` as the instruction.\n"
        '> Strip the leading `r-` prefix when routing (e.g. `r-chat list` → `chat route "list"`).\n\n'
    ]
    for cmd in arg_cmds:
        hint_line = f"**Args:** `{cmd.argument_hint}`\n\n" if cmd.argument_hint else ""
        exec_display = cmd.exec_line.replace('"$ARGUMENTS"', '"<args>"')
        extra = _body_extra(cmd)
        extra_block = f"\n{extra}\n" if extra else ""
        parts.append(
            f"### `/{cmd.r_name}` — {cmd.description}\n\n"
            f"{hint_line}"
            f"```bash\ncd {repo_root}\n{exec_display}\n```\n"
            f"{extra_block}\n"
        )
    return "".join(parts)


def _build_ai_guided_section(cmds: list[PromptCommand]) -> str:
    """Build the AI-guided workflows section."""
    ai_cmds = [c for c in cmds if c.classification == "ai_guided"]
    if not ai_cmds:
        return ""
    parts = [
        "## AI-Guided Workflows (no direct exec — full AI reasoning required)\n\n"
        "These commands have NO direct shell exec. Hermes drives the full workflow\n"
        "using its tools (`read_file`, `write_file`, `terminal`, etc.) "
        "per the guidance below.\n\n"
    ]
    for cmd in ai_cmds:
        parts.append(f"### `/{cmd.r_name}` — {cmd.description}\n\n{cmd.body}\n\n")
    return "".join(parts)


def _build_ss_note() -> str:
    """Special note for the /r-ss two-step vision workflow."""
    return (
        "## `/r-ss` — Screenshot Workflow (Two Steps)\n\n"
        "`/r-ss` is a `quick_command` that copies the latest screenshot to\n"
        "`screenshots/latest.png` and prints the path.\n\n"
        "After it runs, Hermes MUST also display the image:\n\n"
        "```python\n"
        "vision_analyze(\n"
        '    image_url="$HOME/Development/levonbecker/template_ai_vault/screenshots/latest.png",\n'
        '    question="What does this screenshot show?"\n'
        ")\n"
        "```\n\n"
        "Full flow:\n"
        "1. `/r-ss` quick_command runs → copies screenshot, prints confirmation\n"
        "2. Hermes calls `vision_analyze` on `screenshots/latest.png`\n"
        "3. Hermes describes what it sees and asks how to help\n\n"
    )


def _build_footer() -> str:
    return (
        "---\n\n"
        "*Generated from `.github/prompts/*.prompt.md` — source of truth is the prompt files.*\n"
        "*Re-generate: `uv run --no-sync invoke hermes.sync`*\n"
    )


def generate_skill_md(cmds: list[PromptCommand]) -> str:
    """Return the full SKILL.md content string."""
    repo = str(REPO_ROOT)
    return "".join(
        [
            _SKILL_HEADER_TEMPLATE.format(repo_root=repo),
            _build_ss_note(),
            _build_exec_section(cmds),
            _build_exec_long_section(cmds),
            _build_arg_section(cmds, repo),
            _build_ai_guided_section(cmds),
            _build_footer(),
        ]
    )


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------


def write_quick_commands(qc: dict) -> None:
    """Patch the quick_commands key in ~/.hermes/config.yaml."""
    if not HERMES_CONFIG.exists():
        print(f"WARNING: {HERMES_CONFIG} not found — skipping config patch", file=sys.stderr)
        return

    text = HERMES_CONFIG.read_text(encoding="utf-8")

    # Render new block (strip trailing newline — we manage spacing ourselves)
    qc_yaml = yaml.dump({"quick_commands": qc}, default_flow_style=False, sort_keys=True).rstrip()

    # Replace existing quick_commands block (handles both `{}` and multi-line indented form)
    new_lines: list[str] = []
    in_qc_block = False
    inserted = False

    for line in text.splitlines(keepends=True):
        if line.startswith("quick_commands:"):
            new_lines.append(qc_yaml + "\n")
            in_qc_block = True
            inserted = True
            continue
        if in_qc_block:
            # Skip lines that belong to the old block (indented or blank)
            if line.startswith(" ") or line.rstrip() == "":
                continue
            in_qc_block = False
            new_lines.append(line)
        else:
            new_lines.append(line)

    if not inserted:
        new_lines.append("\n" + qc_yaml + "\n")

    HERMES_CONFIG.write_text("".join(new_lines), encoding="utf-8")
    print(f"✅ quick_commands written to {HERMES_CONFIG}")


def write_skill(skill_md: str) -> None:
    """Write SKILL.md to ~/.hermes/skills/r-research/SKILL.md."""
    HERMES_SKILL_DIR.mkdir(parents=True, exist_ok=True)
    HERMES_SKILL_FILE.write_text(skill_md, encoding="utf-8")
    print(f"✅ SKILL.md written to {HERMES_SKILL_FILE}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Read prompts, classify, write quick_commands + SKILL.md."""
    if not PROMPTS_DIR.exists():
        print(f"ERROR: prompts dir not found: {PROMPTS_DIR}", file=sys.stderr)
        sys.exit(1)

    cmds = load_commands()

    print(f"📖 Found {len(cmds)} commands in {PROMPTS_DIR.relative_to(REPO_ROOT)}")
    for cmd in cmds:
        print(f"   [{cmd.classification:10s}] /{cmd.r_name:25s} — {cmd.description}")

    print()
    qc = generate_quick_commands(cmds)
    skill_md = generate_skill_md(cmds)

    write_quick_commands(qc)
    write_skill(skill_md)

    print()
    print("✅ Hermes sync complete.")
    print(f"   quick_commands : {len(qc)} entries")
    print(f"   SKILL.md       : {len(skill_md):,} chars")
    print()
    print("Next steps:")
    print("  1. Start a new Hermes session (or /reset) to pick up quick_commands")
    print("  2. Type /r-research to confirm skill is loaded")
    print("  3. Type /r-pull to test a quick_command")


if __name__ == "__main__":
    main()
