# Cline Module

Generates `.clinerules/workflows/*.md` from `.github/prompts/*.prompt.md`, the source of truth for
all slash commands.

## Overview

Cline has no native slash-command frontmatter format, no `applyTo`-style scoping, and no inline
`!`...`` execution syntax — its workflow files are plain markdown bodies. `sync.py` reads every
prompt file, converts `!`...`` exec lines into "Run this terminal command:" + fenced code block,
and writes the result to `.clinerules/workflows/`.

`claude` is skipped: its filename collides with Claude Code's own `CLAUDE.md` auto-loading
convention on case-insensitive filesystems (APFS).

## Usage

```bash
uv run --no-sync python -m modules.cline.sync
uv run --no-sync invoke cline.sync
```

Never hand-edit `.clinerules/workflows/` — re-run this sync after adding or modifying any
`.github/prompts/*.prompt.md` file, then reload the Cline extension to pick up new workflows.

## Files

- `sync.py` — reads `.github/prompts/` via `modules/common/prompt_commands.py`, writes
  `.clinerules/workflows/*.md`
- `README.md` — this file

## Architecture

```
uv run --no-sync invoke cline.sync
  ↓
modules/cline/sync.py
  ↓
modules/common/prompt_commands.py (shared .prompt.md parser)
  ↓
.clinerules/workflows/*.md
```
