# OpenCode Module

Generates `.opencode/command/*.md` from `.github/prompts/*.prompt.md`, the source of truth for
all slash commands.

## Overview

By default only writes NEW commands (files that don't exist yet). Use `--force` to overwrite
existing hand-crafted command files. Unlike `claude/sync.py` and `cline/sync.py`, `claude` is
**not** skipped here — `/claude` legitimately proxies to the real `claude` CLI from within
OpenCode, with no circularity or filesystem-collision concern.

## Usage

```bash
uv run --no-sync python -m modules.opencode.sync          # additive only
uv run --no-sync python -m modules.opencode.sync --force  # overwrite all
uv run --no-sync invoke opencode.sync
uv run --no-sync invoke opencode.sync --force
```

Never hand-edit `.opencode/command/` — re-run this sync after adding or modifying any
`.github/prompts/*.prompt.md` file, then restart OpenCode to pick up new commands.

## Files

- `sync.py` — reads `.github/prompts/` via `modules/common/prompt_commands.py`, writes
  `.opencode/command/*.md`
- `README.md` — this file

## Architecture

```
uv run --no-sync invoke opencode.sync
  ↓
modules/opencode/sync.py
  ↓
modules/common/prompt_commands.py (shared .prompt.md parser)
  ↓
.opencode/command/*.md
```
