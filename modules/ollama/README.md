# Ollama Module

Local LLM setup and maintenance on Apple Silicon — invoke-only, no slash command.

## Overview

Unlike most modules, Ollama has no `route.py` and no slash command: it's used exclusively via
`invoke ollama.<task>` (see `tasks/ollama.py`), since local-model management is a machine-setup
concern rather than something an AI agent drives interactively.

## Usage

```bash
uv run --no-sync invoke ollama.install   # install Ollama + a local coding LLM
uv run --no-sync invoke ollama.list      # list installed and available models
uv run --no-sync invoke ollama.status    # show service + running-model status
uv run --no-sync invoke ollama.update    # update binary + models + cleanup orphaned blobs
uv run --no-sync invoke ollama.uninstall # uninstall Ollama + remove all models
uv run --no-sync invoke ollama.clean     # remove all downloaded models and blob cache
uv run --no-sync invoke ollama.start     # start the Ollama service via Homebrew
uv run --no-sync invoke ollama.stop      # stop the Ollama service via Homebrew
uv run --no-sync invoke ollama.restart   # restart the Ollama service via Homebrew
```

## Files

- `install.py` — install Ollama + a local coding LLM
- `list.py` — list installed and available models
- `status.py` — show service + running-model status
- `uninstall.py` — uninstall Ollama + remove all models
- `update.py` — update binary + models + cleanup orphaned blobs
- `clean.py` — remove all downloaded models and blob cache
- `helpers.py` — shared helpers (`pull_model` via the Ollama REST API, terminal input helpers)
- `README.md` — this file

## Architecture

```
uv run --no-sync invoke ollama.<task>
  ↓
tasks/ollama.py
  ↓
modules/ollama/<task>.py
```
