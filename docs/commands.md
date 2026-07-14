# Command Reference
Every command below has an equivalent file in `.claude/commands/`, `.opencode/command/`,
`.clinerules/workflows/`, and `.github/prompts/` — the last one is the source of truth. See
[`custom_prompts.md`](custom_prompts.md) for how that sync works.

## Chat
| Command | Purpose | Details |
|---------|---------|---------|
| `/chat start [title]` | Create new conversation | Auto-ends active chat, creates `YYYYMMDD_title.md` in `chats/` |
| `/chat resume [pattern]` | Switch to a different conversation | Filters by filename/date/pattern, prompts for selection |
| `/chat list` | List all chats | Shows all chats in the current topic |
| `/chat end` | End conversation | Writes the full log to the chat file, clears active status; does not commit or push |

## Topic
| Command | Purpose | Details |
|---------|---------|---------|
| `/topic list` | Show active topic | |
| `/topic list all` | Show full topic tree | Marks the active topic |
| `/topic switch <path>` / `/topic <path>` | Switch to a topic | Auto-saves current chat, switches context, resumes active chat |
| `/topic new <path> [description]` | Create + initialize a new topic | |
| `/topic init [description]` | Initialize the current directory as a topic | |
| `/topic update [--dry-run] [--current-only]` | Regenerate topic `AGENTS.md` files | Rolls out template changes across all topics |

## Repo & Screenshots
| Command | Purpose | Details |
|---------|---------|---------|
| `/push` | Push changes | Runs `invoke fix` + `invoke test`, then commits and pushes |
| `/pull` | Pull updates | Stashes local changes, pulls with rebase, restores stash |
| `/repo cleanup` | Remove old screenshots | Deletes all screenshots except `latest.png` |
| `/repo set_screenshots` | Configure screenshot location | Sets macOS to save screenshots to the central folder |
| `/ss` / `/repo view_screenshot` | View latest screenshot | Copies latest screenshot to `latest.png` and reads it — see [`screenshots.md`](screenshots.md) |

`/repo <subcommand>` is the umbrella form (`push`, `pull`, `cleanup`, `set_screenshots`,
`view_screenshot`); `/push`, `/pull`, and `/ss` are standalone top-level commands that call the same
underlying module.

## Feature Branch / PR Workflow
Independent of `/push` and `/pull` (which handle the primary tracked branch) — use these when
working on a feature branch that needs a GitHub Pull Request.

| Command | Purpose | Details |
|---------|---------|---------|
| `/pr-notes` | Draft PR notes | Compares current branch to its base (`development`/`main`), saves a `## Summary` / `## Changes` draft to `tmp/pull_requests/` — does not push or open a PR |
| `/pr` | Draft + open a PR | Same diff/notes drafting as `/pr-notes`, but opens the PR directly via `gh pr create` — does not push |
| `/rebase` | Rebase onto remote default branch | Optionally runs `/squash` first; handles stashing and interactive conflict resolution |
| `/squash` | Squash all commits to root | Anchored squash into one commit with an auto-generated message; prompts to confirm and optionally force-push |
| `/punch-it-chewy` | Push + draft PR + open PR | Combines a feature-branch push (fix → test → commit → push) with `/pr` in one command |

Requires `gh` (GitHub CLI) authenticated — see [`setup.md`](setup.md).

## Setup, Testing & Sync
| Command | Purpose | Details |
|---------|---------|---------|
| `/setup` | Run initial project setup | Runs `./setup.sh` (macOS) — creates `.venv`, installs deps, and configures `properties.yml` via `inv setup.properties` |
| `/fix` | Auto-fix lint issues | `ruff check --fix` + `ruff format` |
| `/test` | Run all tests and linters | ruff, pylint, yamllint, actionlint — must be 10/10 for `.py`/`.yml` changes |
| `/sync-setup` | Pull shared tooling updates | Compares this repo against the `template_python` skeleton repo (`modules/`, `tasks/`, `.github/`, `.claude/`, config files) and syncs in changes, asking about anything ambiguous |

## Version Management
| Command | Purpose | Details |
|---------|---------|---------|
| `/versioning [libs \| workflows \| all]` | Check for updates | Read-only — checks `pyproject.toml` deps and `.github/workflows/` action refs against latest releases, updates version *locks* only. Does not install or run anything |
| `/upgrade [python \| libs]` | Install updates | Executes the actual upgrade: installs Python, rebuilds `.venv`, runs `uv sync --upgrade` |

**Workflow**: run `/versioning` to review and lock updates → check `git diff` → run `/upgrade` to
install.

## Other Tools
| Command | Purpose | Details |
|---------|---------|---------|
| `/claude [args]` | Run Claude Code CLI directly | Proxies to the `claude` CLI using your Pro/Max subscription — see `modules/claude/README.md` |

Ollama (local LLM) has no slash command — it's invoke-task-only: `inv ollama.install` /
`inv ollama.list` / `inv ollama.status` / `inv ollama.update` / `inv ollama.uninstall`.

## Testing Commands Directly
Every slash command has an equivalent that runs without an AI tool:

```bash
cd $HOME/Development/levonbecker/template_ai_vault
source .venv/bin/activate

# Chat management
uv run --no-sync python -m modules.chat.start --title="test title"
uv run --no-sync python -m modules.chat.list
uv run --no-sync python -m modules.chat.resume --pattern="pattern"

# Topic management
uv run --no-sync python -m modules.topic.list
uv run --no-sync python -m modules.topic.new --path health/dental

# Repository management
uv run --no-sync python -m modules.repo.cleanup
uv run --no-sync python -m modules.repo.pull
uv run --no-sync python -m modules.repo.push
uv run --no-sync python -m modules.repo.set_screenshots
uv run --no-sync python -m modules.repo.view_screenshot

# Versioning
uv run --no-sync invoke versioning.all --dry-run
uv run --no-sync invoke upgrade
```
