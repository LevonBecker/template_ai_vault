---
applyTo: "modules/**"
---
# Python Modules Instructions

## Architecture

**Commands are thin wrappers. Logic lives in Python modules.**

```
User → AI Tool Slash Command → Router Module → Python Module
        (tool command dir)       (modules/*)     (modules/)
```

## Module Organization

```
modules/
├── chat/         # Chat lifecycle (start, end, resume, list)
├── topic/        # Topic navigation and setup (init, switch, update, templates)
├── repo/         # Repository maintenance (push, pull, cleanup, screenshots)
├── accounting/   # Expense tracking and cost calculation
└── common/       # Shared utilities (cli, utils, properties, route_utils)
```

## Mandatory Standards

### Named Options Only (NO positional arguments)

```python
# ✅ CORRECT
@cli.command()
@cli.option("--title", default=None, help="Title for the chat")
def main(title: str | None = None):
    pass

# ❌ WRONG — never use positional arguments
def main(title):
    pass
```

### Path Resolution

Always use `modules/repo/fetch_properties.py` — never hardcode paths:

```python
from ..repo.fetch_properties import get_repo_local, get_screenshots_location

repo_root = get_repo_local()
screenshots = get_screenshots_location()
```

### Inter-Module Import Rules

- `common/` utilities: importable from any module
- `repo/fetch_properties.py`: importable from any module
- No cross-imports between `chat/`, `topic/`, `repo/`, `accounting/`
- If truly shared: move to `common/`

## Code Quality

All Python changes must achieve 10/10 before any commit. See `.github/instructions/tests.instructions.md`.

**Fix issues. Never disable linter warnings without user approval.**

## templates.py Change Rule

`modules/topic/templates.py` is the single source of truth for all topic instruction file content (OPENCODE.md). It drives what gets generated when `/topic init` or `/topic update` runs.

**When you modify `templates.py`:**
1. Run fix + test as usual (10/10 required)
2. **Ask the user**: "Should I run `/topic update` to regenerate all topic AGENTS.md files with the new template?"
3. Also **check whether `AGENTS.md` (repo root) needs manual sync** — root AGENTS.md is hand-maintained and may need the same rule added if the template change reflects a new policy

## Common CLI Option Patterns

```python
# Optional string
@cli.option("--title", default=None, help="Title for the chat")

# Required string
@cli.option("--path", required=True, help="Path to topic")

# Boolean flag
@cli.option("--yes", "-y", is_flag=True, help="Skip confirmation")

# Integer with default
@cli.option("--count", default=20, help="Number of items")

# Choice from list
@cli.option("--sort", type=cli.Choice(["newest", "oldest"]), default="newest")

# Path that must exist
@cli.option("--file", type=cli.Path(exists=True), help="Input file")
```

### What `modules.common.cli` Provides

- **Automatic parsing** — Converts CLI strings to Python types
- **Help generation** — Auto-generates `--help` documentation
- **Type validation** — Ensures correct types (string, int, bool, Path)
- **Default values** — Handles optional parameters elegantly
- **Error handling** — User-friendly error messages

## Module File Reference

```
modules/
├── chat/
│   ├── active.py       # Active chat state (active.yml)
│   ├── end.py
│   ├── list.py
│   ├── resume.py
│   ├── route.py        # /chat routing
│   └── start.py
├── claude/
│   ├── route.py        # /claude routing (proxies to claude CLI)
│   └── sync.py         # Syncs .claude/commands/ from .github/prompts/
├── cline/
│   └── sync.py         # Syncs .clinerules/workflows/ from .github/prompts/
├── hermes/
│   └── sync.py         # Syncs ~/.hermes/ config + SKILL.md from .github/prompts/
├── ollama/
│   ├── helpers.py      # Shared helpers (pull_model via Ollama REST API)
│   ├── install.py      # Install Ollama + local coding LLM on Apple Silicon
│   ├── list.py         # List installed and available models
│   ├── status.py       # Show service + running-model status
│   ├── uninstall.py    # Uninstall Ollama + remove all models
│   └── update.py       # Update binary + models + cleanup orphaned blobs
├── opencode/
│   └── sync.py         # Syncs .opencode/command/ from .github/prompts/
├── repo/
│   ├── cleanup.py
│   ├── fetch_properties.py  # Central properties loader — use for all paths
│   ├── pull.py
│   ├── push.py
│   ├── route.py
│   ├── set_screenshots.py
│   └── view_screenshot.py
├── topic/
│   ├── active.py       # Active topic state (active_topic.yml)
│   ├── init.py
│   ├── list.py
│   ├── new.py
│   ├── route.py        # /topic routing
│   ├── switch.py
│   ├── templates.py    # Single source of truth for OPENCODE.md content
│   │                   # ⚠️  See topics.instructions.md → "templates.py Change Rule" when modifying this file.
│   ├── update.py
│   └── update_list.py
└── common/
    ├── cli.py            # Click-based CLI wrapper
    ├── invoke_runner.py
    ├── properties.py
    ├── route_utils.py    # find_repo_root, build_env
    └── utils.py
```

## AI Tool Sync Modules

`.github/prompts/` is the single source of truth for all slash commands. Three sync modules generate the tool-specific formats from it:

| Module | Output | Invoke command |
|---|---|---|
| `modules/claude/sync.py` | `.claude/commands/*.md` | `inv claude.sync` |
| `modules/cline/sync.py` | `.clinerules/workflows/*.md` | `inv cline.sync` |
| `modules/hermes/sync.py` | `~/.hermes/config.yaml` + `SKILL.md` | `inv hermes.sync` |
| `modules/opencode/sync.py` | `.opencode/command/*.md` | `inv opencode.sync` |

Run `inv ai.sync` to regenerate all four at once. Never hand-edit the output dirs.

## Module Template

```python
"""
Module description.

Usage:
    uv run --no-sync python -m modules.<group>.<name> [--option value]
"""
from modules.common import cli
from modules.repo.fetch_properties import get_repo_local


@cli.command()
@cli.option("--argument", default=None, help="Description of argument")
def main(argument: str | None = None) -> None:
    """One-line summary of what this module does."""
    repo_root = get_repo_local()
    cli.echo(f"Repo root: {repo_root}")
    # Business logic here


if __name__ == "__main__":
    main()
```
