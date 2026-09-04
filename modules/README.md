# Modules
Reusable Python modules imported by `tasks/*.py` invoke tasks and by the AI-tool command routers
(`modules/*/route.py`). All functions are module-level — no classes required except small helper
validators in `common/cli.py`.

## Structure
```
modules/
  chat/         # research chat session lifecycle (start, resume, end, list, active)
  common/       # cli, properties, utils, route_utils, prompt_commands, chat_state, invoke_runner helpers
  docs/         # changelog sync — docs/change_logs/ vs properties.yml
  hermes/       # generates ~/.hermes/ config + SKILL.md from .github/prompts/
  ollama/       # local LLM setup/maintenance on Apple Silicon (invoke tasks only, no slash command)
  opencode/     # generates .opencode/command/ from .github/prompts/
  repo/         # git workflow, screenshot handling, PR diff/notes/create/cleanup
  setup/        # creates/stamps properties.yml, called by setup.sh/setup.ps1
  template/     # sync shared, generic tooling with the parent template repo for /template
  topic/        # topic directory navigation, init, switch, and AGENTS.md/OPENCODE.md generation
  versioning/   # dependency locks, Python version, and workflow action-ref checks
```

## Submodules
| Directory | Purpose |
|-----------|---------|
| [`chat/`](chat/README.md) | Research chat session lifecycle — start, resume, end, list, active state |
| [`common/`](common/README.md) | CLI helpers, `properties.yml` config reader, output/utility helpers, shared prompt/chat-state parsing |
| [`docs/`](docs/README.md) | Changelog sync — `docs/change_logs/` vs `properties.yml` |
| [`hermes/`](hermes/README.md) | Generates the Hermes `quick_commands` config + `r-research` `SKILL.md` from `.github/prompts/` |
| [`ollama/`](ollama/README.md) | Local LLM install/list/update/uninstall/status on Apple Silicon |
| [`opencode/`](opencode/README.md) | Generates `.opencode/command/*.md` from `.github/prompts/*.prompt.md` |
| [`repo/`](repo/README.md) | Git workflow (pull, push, squash, rebase, PR), screenshot cleanup/view |
| [`setup/`](setup/README.md) | Creates/stamps `properties.yml`, called by `setup.sh`/`setup.ps1` |
| [`template/`](template/README.md) | Sync shared, generic tooling with the parent template repo for `/template` |
| [`topic/`](topic/README.md) | Topic directory navigation, init, switch, and instruction-file generation |
| [`versioning/`](versioning/README.md) | Dependency lock and workflow action-ref checks (no `VERSION`-bump tasks — this repo doesn't ship releases) |

Repo-consistency checks (`check_agents`) live under root `tests/` as pytest tests, not here — see
`../tests/test_check_agents.py` and `.github/instructions/tests.instructions.md`.

## Conventions
- One module per file; filename matches the concern in snake_case
- Each `route.py` file exposes a `main()` entry point and dispatches its slash command's subcommands
- Shell out via `subprocess.run(..., cwd=repo_path)` — never `shell=True`
- Use `modules.common.utils` (`success`/`error`/`warning`/`info`) for all console output
- Resolve repo config via `modules.common.properties`
