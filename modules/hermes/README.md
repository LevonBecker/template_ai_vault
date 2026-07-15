# Hermes Module

Generates the `quick_commands` block in `~/.hermes/config.yaml` and a full `r-research`
`SKILL.md` from `.github/prompts/*.prompt.md`, the source of truth for all slash commands.

## Overview

Hermes has no native prompt-file format at all — it's driven entirely by `~/.hermes/config.yaml`
(zero-token `quick_commands`) and skill files. `sync.py` reads every prompt file via
`modules/common/prompt_commands.py`, classifies each one (`exec` / `exec_long` / `arg` /
`ai_guided`) based on its own Hermes-specific rules (e.g. which commands are too long-running for
the 30s `quick_commands` timeout), and writes both output files.

`claude` is skipped — not useful as a Hermes `/r-*` command.

## Usage

```bash
uv run --no-sync python -m modules.hermes.sync
uv run --no-sync invoke hermes.sync
```

Never hand-edit `~/.hermes/config.yaml`'s `quick_commands` key or the generated `SKILL.md` — re-run
this sync after adding or modifying any `.github/prompts/*.prompt.md` file, then start a new Hermes
session (or `/reset`) to pick up the changes.

## Files

- `sync.py` — reads `.github/prompts/` via `modules/common/prompt_commands.py`, classifies
  commands, and writes `~/.hermes/config.yaml` + `~/.hermes/skills/r-research/SKILL.md`
- `README.md` — this file

## Architecture

```
uv run --no-sync invoke hermes.sync
  ↓
modules/hermes/sync.py
  ↓
modules/common/prompt_commands.py (shared .prompt.md parser)
  ↓
~/.hermes/config.yaml (quick_commands) + ~/.hermes/skills/r-research/SKILL.md
```
