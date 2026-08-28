---
applyTo: "tasks/**"
---
# Tasks Instructions

## Overview

Invoke is the task runner for CICD workflows (fix, test, upgrade). All tasks are defined in `tasks/` and called via `uv run --no-sync invoke <task>`. Never use invoke for business logic — business logic lives in Python modules.

Unlike `.github/prompts/*.prompt.md` (which capture AI/human decision-making — see
`.github/instructions/logic.instructions.md`), invoke tasks are deterministic CLI automation only:
no judgment calls, no AI-specific behavior.

## Combo Tasks (use these most often)

| Task | Command | Description |
|------|---------|-------------|
| AI Sync | `uv run --no-sync invoke ai.sync` | Sync all AI tool commands from `.github/prompts/` |
| Fix | `uv run --no-sync invoke fix` | Run all auto-fixes (ruff fix + format) |
| Test | `uv run --no-sync invoke test` | Run all tests (actionlint + check_agents + pylint + pytest + ruff + yamllint) |

## Test Tasks

Lives in `tasks/tests/` — one file per check, still registered as one flat `tests.*` namespace.
Pass `scope=<marker>` to `tests.pytest` to run a subset (e.g. `scope=hermes`, `scope=topic`,
`scope="not style"`) — matches the pytest marker each `tests/<folder>/` corresponds to (see
`tests.instructions.md`).

| Task | Command | Description |
|------|---------|-------------|
| actionlint | `uv run --no-sync invoke tests.actionlint` | GitHub Actions workflow validation |
| check_agents | `uv run --no-sync invoke tests.check_agents` | Verify `.github/prompts/` mirrors stay in sync (`pytest -m "agents"`, i.e. `tests/agents/`) |
| pylint | `uv run --no-sync invoke tests.pylint` | Python code quality |
| pytest | `uv run --no-sync invoke tests.pytest` | Python unit test suite |
| rufflint | `uv run --no-sync invoke tests.rufflint` | Python linting and formatting |
| yamllint | `uv run --no-sync invoke tests.yamllint` | YAML file validation |

## Repo Tasks

Lives in `tasks/ai/repo.py` — wraps `modules/repo/*.py` (git/PR workflow, screenshot tooling).

| Task | Command | Description |
|------|---------|-------------|
| cleanup | `uv run --no-sync invoke repo.cleanup` | Delete merged local branches |
| pull | `uv run --no-sync invoke repo.pull` | Pull updates from git remote (stash → pull --rebase → restore) |
| push | `uv run --no-sync invoke repo.push` | Push to git remote and iCloud Obsidian folder (fix → test → commit → push) |
| pr_push | `uv run --no-sync invoke repo.pr_push` | Push the current feature branch |
| rebase | `uv run --no-sync invoke repo.rebase` | Rebase onto remote default branch (optionally squash first) |
| squash | `uv run --no-sync invoke repo.squash` | Anchored squash of all commits to root, optional force push |
| pr_diff | `uv run --no-sync invoke repo.pr_diff` | Show current branch's commit log/diff vs. its base branch |
| pr_notes_save | `uv run --no-sync invoke repo.pr_notes_save` | Save PR notes to `tmp/pull_requests/` |
| pr_create | `uv run --no-sync invoke repo.pr_create` | Open a GitHub PR for the current branch |
| pr_cleanup | `uv run --no-sync invoke repo.pr_cleanup` | Switch to default branch, pull, delete the merged feature branch |
| set_screenshots | `uv run --no-sync invoke repo.set_screenshots` | Set up the screenshots/ workflow for this repo |
| view_screenshot | `uv run --no-sync invoke repo.view_screenshot` | View the most recent screenshot |

## Template Tasks

Lives in `tasks/ai/template.py` — wraps `modules/template/*.py` (parent-template sync).

| Task | Command | Description |
|------|---------|-------------|
| pull | `uv run --no-sync invoke template.pull` | Resolve the local path to the parent template repo |
| push_diff | `uv run --no-sync invoke template.push_diff` | Diff this repo's scoped tooling against the parent template repo |
| push_apply | `uv run --no-sync invoke template.push_apply` | Copy approved files/deletions to a new branch upstream |
| push_create_pr | `uv run --no-sync invoke template.push_create_pr` | Open a PR for that branch against the parent template repo |

## Ai Vault Tasks

Lives in `tasks/ai_vault/{chat,topic}.py` — this repo's own reason for existing: dated
planning-chat logging and topic workspace management. Backs `/chat` and `/topic`.

| Task | Command | Description |
|------|---------|-------------|
| chat.start | `uv run --no-sync invoke chat.start` | Start a new dated planning chat in the active topic |
| chat.end | `uv run --no-sync invoke chat.end` | Validate the active chat has real content, clear its tracker |
| chat.list | `uv run --no-sync invoke chat.list` | Show every chat file in the active topic |
| chat.resume | `uv run --no-sync invoke chat.resume` | Reopen the chat matching a filename/title pattern |
| topic.init | `uv run --no-sync invoke topic.init` | Initialize topic structure in the current directory |
| topic.list | `uv run --no-sync invoke topic.list` | Show the active topic, or every topic with `--show-all` |
| topic.new | `uv run --no-sync invoke topic.new` | Create a new topic at `topics/<path>` |
| topic.switch | `uv run --no-sync invoke topic.switch` | Switch the active topic, auto-saving any active chat first |
| topic.update | `uv run --no-sync invoke topic.update` | Regenerate AGENTS.md/CLAUDE.md for every topic |

## Ruff Tasks

| Task | Command | Description |
|------|---------|-------------|
| fix | `uv run --no-sync invoke ruff.fix` | Auto-fix ruff lint issues |
| format | `uv run --no-sync invoke ruff.format` | Auto-format Python code |

## Upgrade Tasks

| Task | Command | Description |
|------|---------|-------------|
| libs | `uv run --no-sync invoke upgrade.libs` | Upgrade libraries only |
| python | `uv run --no-sync invoke upgrade.python` | Upgrade Python only |
| sync | `uv run --no-sync invoke upgrade.sync` | Sync dependencies (no version check) |
| upgrade | `uv run --no-sync invoke upgrade.upgrade` | Upgrade Python + all dependencies (default) |

## uv Tasks

| Task | Command | Description |
|------|---------|-------------|
| upgrade_bin | `uv run --no-sync invoke uv.upgrade_bin` | Upgrade the uv binary itself (`brew upgrade uv`) |
| upgrade_libs | `uv run --no-sync invoke uv.upgrade_libs` | Install the versions currently locked in `pyproject.toml` (`uv sync`) |

## Versioning Tasks

Read-only version-lock *checks* — compare `pyproject.toml` deps and `.github/workflows/` action
refs against latest releases and update the version locks in place (does not install anything;
see Upgrade Tasks above for that).

| Task | Command | Description |
|------|---------|-------------|
| update | `uv run --no-sync invoke ver.update` | Run every version check (libs, python, workflows) |
| libs | `uv run --no-sync invoke ver.libs` | Check `pyproject.toml` deps against latest releases |
| python | `uv run --no-sync invoke ver.python` | Check the pinned Python version against the latest release |
| workflows | `uv run --no-sync invoke ver.workflows` | Check `.github/workflows/` action refs against latest versions |
| project_bump_patch | `uv run --no-sync invoke ver.project_bump_patch` | Bump root `VERSION` patch — every merge to development |
| project_bump_minor | `uv run --no-sync invoke ver.project_bump_minor` | Bump `VERSION` minor — a milestone release |
| project_bump_major | `uv run --no-sync invoke ver.project_bump_major` | Bump `VERSION` major — a major release |
| project_bump_build | `uv run --no-sync invoke ver.project_bump_build` | `VERSION` build counter — feature-branch only, never published |

## Invoke vs Direct Python

| Use case | Command |
|----------|---------|
| Fix code style | `uv run --no-sync invoke fix` |
| Run all tests | `uv run --no-sync invoke test` |
| Run one linter | `uv run --no-sync invoke tests.pylint` |
| Upgrade everything | `uv run --no-sync invoke upgrade.upgrade` |
| Run a module | `uv run --no-sync python -m modules.chat.start --title="..."` |
| Test a route | `uv run --no-sync python -m modules.chat.route "start my chat"` |

## Canonical Workflow

```bash
# After modifying Python or YAML files:
uv run --no-sync invoke fix    # auto-fix first
uv run --no-sync invoke test   # verify 10/10
```

All `uv run` calls MUST use `--no-sync`. See `.github/instructions/tests.instructions.md`.

## AI Sync Tasks

Lives in `tasks/ai/{hermes,opencode}.py`. `.github/prompts/` is the source of truth for all slash
commands. Run after adding or modifying any `.github/prompts/*.prompt.md` file.

| Task | Command | Description |
|------|---------|-------------|
| sync all | `uv run --no-sync invoke ai.sync` | Sync all AI tools at once (runs both below) |
| hermes | `uv run --no-sync invoke hermes.sync` | Sync `~/.hermes/` config + SKILL.md |
| opencode | `uv run --no-sync invoke opencode.sync` | Sync `.opencode/command/` |

`.claude/commands/` and `.clinerules/workflows/` have no sync task — they're hand-maintained
mirrors, checked by `tests.check_agents` (below).

## Ollama Tasks

Lives in `tasks/ai/ollama.py`.

| Task | Command | Description |
|------|---------|-------------|
| clean | `uv run --no-sync invoke ollama.clean` | Remove all downloaded models and blob cache |
| install | `uv run --no-sync invoke ollama.install` | Install Ollama + a local coding LLM |
| list | `uv run --no-sync invoke ollama.list` | List installed and available models |
| restart | `uv run --no-sync invoke ollama.restart` | Restart Ollama service via Homebrew |
| start | `uv run --no-sync invoke ollama.start` | Start Ollama service via Homebrew |
| status | `uv run --no-sync invoke ollama.status` | Show Ollama service and running-model status |
| stop | `uv run --no-sync invoke ollama.stop` | Stop Ollama service via Homebrew |
| uninstall | `uv run --no-sync invoke ollama.uninstall` | Uninstall Ollama and remove all models |
| update | `uv run --no-sync invoke ollama.update` | Update Ollama binary + all installed models |

## Docs Tasks

Lives in `tasks/ai/docs.py`. Runs as part of `invoke fix` and `/docs` — see
`.github/instructions/docs.instructions.md`.

| Task | Command | Description |
|------|---------|-------------|
| update_changelogs | `uv run --no-sync invoke docs.update_changelogs` | Prepend any missing `docs/change_logs/<category>/<name>.md` entries from `properties.yml` |

## Task Ordering

Tasks within a file must be ordered **alphabetically by function name**. Do not order by addition date, logical grouping, or importance.

## Task File Locations

```
tasks/
├── __init__.py      # Wires the invoke Collection: ai/, ai_vault/, common/ (each registered at
│                     # their original top-level names — grouped for file organization only, not
│                     # nested namespaces), plus tests/
├── ai/              # Tooling this repo uses to operate on itself, or to integrate with a
│   │                 # specific AI tool
│   ├── docs.py      # docs.update_changelogs
│   ├── hermes.py    # hermes.sync — syncs ~/.hermes/ config + SKILL.md
│   ├── ollama.py    # ollama.install/list/update/uninstall/start/stop/status/restart/clean
│   ├── opencode.py  # opencode.sync — syncs .opencode/command/
│   ├── repo.py      # repo.pull, repo.push, repo.pr_*, repo.squash, repo.rebase, repo.*screenshot*
│   └── template.py  # template.pull, template.push_diff, template.push_apply, template.push_create_pr
├── ai_vault/        # This repo's own reason for existing
│   ├── chat.py      # chat.start, chat.end, chat.list, chat.resume
│   └── topic.py     # topic.init, topic.list, topic.new, topic.switch, topic.update
├── common/          # template_python-inherited boilerplate
│   ├── main.py      # fix, test, ai.sync combo tasks (was combos.py)
│   ├── debug.py     # debug utilities
│   ├── ruff.py      # ruff.fix + ruff.format
│   ├── setup.py     # setup.properties — creates/stamps properties.yml
│   ├── upgrade.py   # libs, python, sync, upgrade
│   ├── uv.py        # uv.upgrade_bin, uv.upgrade_libs
│   └── versioning.py # all, libs, workflows (version-lock checks)
└── tests/           # One file per check (actionlint.py, check_agents.py, pylint.py, pytest.py,
                      # rufflint.py, yamllint.py) — still one flat tests.* namespace
```

`repo.py`/`template.py` wrap `modules/repo/`/`modules/template/`, which existed before but had no
`invoke` task exposing them directly (only reachable via the prompt/skill router) — newly wired
2026-08-11, alongside `chat.py`/`topic.py` for the same reason. All four use
`context.run("python -m modules....")`, matching every other task here — this repo's
`tasks/__init__.py` never adds the repo root to `sys.path`, so a direct `from modules.x import y`
import would fail inside the invoke process itself (subprocess resolves fine since Python's own
`-m` uses the CWD).
