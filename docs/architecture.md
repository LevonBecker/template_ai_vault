# Architecture
How the repo's multi-tool automation is built: repository layout, the command/logic split, and how
rules and slash commands stay in sync across every AI tool.

## Repository Structure
```
template_ai_vault/
├── topics/                                    # Research topics organized hierarchically
│   ├── travel/                               # Example: single topic
│   │   ├── chats/                            # Conversation history
│   │   │   ├── 20260104_setup.md
│   │   │   └── 20260105_tutorial.md
│   │   ├── docs/                             # Documentation and notes
│   │   ├── AGENTS.md                         # Topic source of truth (content + context)
│   │   ├── CLAUDE.md                         # Thin pointer to AGENTS.md
│   │   └── active.yml                        # Current active conversation
│   │
│   ├── health/                               # Example: multi-level topic hierarchy (group topic)
│   │   └── dental/                           # Subtopic: Dental
│   │       ├── chats/
│   │       ├── docs/
│   │       ├── AGENTS.md
│   │       ├── CLAUDE.md
│   │       └── active.yml
│   │
│   ├── financials/                           # Group topic: budget, income_tax, investments
│   └── shopping/                             # Single topic — docs/apparel, docs/electronics, docs/auto
│
├── screenshots/                               # Centralized screenshot storage (ALL topics)
│   ├── latest.png                            # Latest screenshot for AI viewing
│   └── Screenshot 2026-01-04 at 3.00.09 PM.png
│
├── modules/                                   # Python modules (all business logic)
├── tasks/                                     # Invoke tasks (CI, sync, linting, upgrades)
│
├── .github/
│   ├── instructions/                         # Source of truth for AI RULES
│   └── prompts/                               # Source of truth for SLASH COMMANDS
├── .claude/commands/                          # Generated — synced from .github/prompts/
├── .opencode/command/                         # Generated — synced from .github/prompts/
├── .clinerules/workflows/                     # Generated — synced from .github/prompts/
│
├── AGENTS.md                                   # Thin pointer for OpenCode → .github/instructions/
└── CLAUDE.md                                   # Thin pointer for Claude → AGENTS.md
```

Topics can be a single flat directory (`topics/travel/`) or a group of subtopics
(`topics/health/dental/`, `topics/health/fitness/`, …) — `topics/health/` itself is just a folder,
not a topic. See `modules/topic/README.md` for topic navigation details.

## Two Separate Sync Systems
This repo keeps AI tools in sync along two independent tracks — don't conflate them:

| | **Rules** (agent behavior) | **Commands** (slash commands) |
|---|---|---|
| Source of truth | `.github/instructions/*.md` | `.github/prompts/*.prompt.md` |
| Read by | Applied natively by GitHub Copilot; delegated to by `AGENTS.md`/`CLAUDE.md` for other tools | Generated into each tool's native command format |
| Sync mechanism | Delegation (pointer files), not file generation | Code generation (`inv *.sync`) |
| Covers | Workflow rules, file placement, coding standards, testing requirements | `/chat`, `/topic`, `/repo`, `/push`, `/ss`, etc. |

### 1. Rules: Instruction File Hierarchy
**`.github/instructions/` is the one and only source of truth for all AI behavior rules.** Never
duplicate rules elsewhere — update the instruction files and let every provider pick them up through
delegation:

| Priority | Provider | Reads | How rules flow in |
|----------|----------|-------|--------------------|
| 1 | **GitHub Copilot** | `.github/instructions/*.md` | Native — `applyTo` frontmatter auto-applies each file to matching paths |
| 2 | **OpenCode** | `AGENTS.md` (repo root) | `AGENTS.md` is a thin pointer; all substance lives in `.github/instructions/` |
| 3 | **Claude Code / Claude TUI** | `CLAUDE.md` → `AGENTS.md` | `CLAUDE.md` delegates to `AGENTS.md`, which delegates to `.github/instructions/` |

Topic-level context works the same way: `topics/*/AGENTS.md` holds topic-scoped content and links
back to the root `AGENTS.md`; `topics/*/CLAUDE.md` is a thin pointer to the topic's `AGENTS.md`.

**Adding a new rules-consuming provider**: if it doesn't natively read `.github/instructions/`,
create a thin entrypoint file that says "See `AGENTS.md` for all instructions" — never copy rules
into it.

### 2. Commands: Prompt File Sync
**`.github/prompts/*.prompt.md` is the single source of truth for every slash command.** Command
*content* is generated from there into each tool's native format — hand-editing a generated file
gets overwritten the next time someone runs `--force`.

| Module | Generates | Invoke command |
|---|---|---|
| `modules/claude/sync.py` | `.claude/commands/*.md` | `inv claude.sync` |
| `modules/cline/sync.py` | `.clinerules/workflows/*.md` | `inv cline.sync` |
| `modules/hermes/sync.py` | `~/.hermes/config.yaml` + `SKILL.md` | `inv hermes.sync` |
| `modules/opencode/sync.py` | `.opencode/command/*.md` | `inv opencode.sync` |

Run `uv run --no-sync invoke ai.sync` to regenerate all four at once. See
[`custom_prompts.md`](custom_prompts.md) for the full workflow (creating a command, editing one,
what "source of truth" means in practice).

## Three-Layer Command Pattern
Every slash command follows the same layering — **commands are thin wrappers; logic lives in Python
modules**:

```
User → AI Tool Slash Command → Router Module → Python Module
        (tool command dir)       (modules/*/route.py)  (modules/*)
```

**Example:**
```
User types: /chat resume wire_tunnels
  ↓
AI tool reads: .opencode/command/chat.md (or .claude/commands/chat.md, etc.)
  ↓
Command file executes: uv run --no-sync python -m modules.chat.route "resume wire_tunnels"
  ↓
Router (modules/chat/route.py) dispatches: modules.chat.resume --pattern="wire_tunnels"
  ↓
Python function receives: pattern="wire_tunnels"
```

- **Layer 1 (Commands)**: `.opencode/command/`, `.claude/commands/`, `.clinerules/workflows/`,
  `.github/prompts/` — thin wrappers only, no business logic
- **Layer 2 (Routers)**: `modules/*/route.py` — parse `$ARGUMENTS`, dispatch to the target module
- **Layer 3 (Modules)**: `modules/*/` — all business logic, reusable and independently testable

## Python Modules
```
modules/
├── chat/                        # Chat lifecycle
│   ├── active.py                # Active chat state (active.yml)
│   ├── start.py / end.py / list.py / resume.py
│   ├── route.py                 # /chat routing
│   └── README.md
├── topic/                       # Topic structure management
│   ├── active.py                # Active topic state (active_topic.yml)
│   ├── new.py / init.py / list.py / switch.py / update.py / update_list.py
│   ├── templates.py             # AGENTS.md content templates — single source of truth for topic docs
│   ├── route.py                 # /topic routing
│   └── README.md
├── repo/                        # Repository + git-flow operations
│   ├── push.py / pull.py / cleanup.py
│   ├── set_screenshots.py / view_screenshot.py
│   ├── pr_diff.py / pr_notes.py / pr_create.py / pr_push.py
│   ├── rebase.py / squash.py
│   ├── route.py                 # /repo routing
│   └── README.md
├── versioning/                  # Dependency + Python version checks (read-only) and upgrades
│   ├── libs.py                  # pyproject.toml deps vs. latest release
│   ├── python.py                # Pinned Python version vs. latest release
│   ├── workflows.py             # .github/workflows/ action refs vs. latest tag
│   ├── check_all.py             # Combined libs + python check
│   ├── upgrade.py / uv_sync.py  # Actual install/sync (used by /upgrade)
│   ├── route.py                 # /versioning routing
│   └── README.md
├── skeleton/                    # Locates the shared template_python skeleton repo for /sync-setup
│   ├── sync.py / route.py
│   └── README.md
├── claude/                      # Claude Code CLI passthrough + command sync
│   ├── route.py                 # /claude → proxies to the `claude` CLI
│   ├── sync.py                  # Generates .claude/commands/ from .github/prompts/
│   └── README.md
├── cline/
│   └── sync.py                  # Generates .clinerules/workflows/ from .github/prompts/
├── hermes/
│   └── sync.py                  # Generates ~/.hermes/ config + SKILL.md from .github/prompts/
├── opencode/
│   └── sync.py                  # Generates .opencode/command/ from .github/prompts/
├── ollama/                      # Local LLM setup on Apple Silicon (invoke tasks only, no slash command)
│   ├── install.py / list.py / status.py / update.py / uninstall.py
│   └── helpers.py
└── common/                      # Shared utilities
    ├── properties.py            # Central properties.yml loader — get_repo_local(), get_screenshots_location(), etc.
    ├── cli.py                   # Click-based CLI wrapper used by every module
    ├── route_utils.py           # find_repo_root(), build_env() — used by every route.py
    └── utils.py                 # success()/error()/warning()/info() console output helpers
```

## Design Principles
1. **Commands are thin wrappers** — all logic lives in Python modules under `modules/`
2. **Python modules do the work** — validation, business logic, error handling
3. **Invoke tasks drive CI and sync** — `tasks/` runs tests, linting, and the `*.sync` generators
4. **Composable & testable** — modules can be tested independently
5. **No side effects outside the repo** — only read/write git-tracked paths (or `~/.hermes/` for
   the Hermes sync target, which is explicitly external by design)
6. **Clear error messages** — emoji prefixes: ✅ ❌ ⚠️ 📂 🎯
7. **Virtual environment** — all Python commands require `.venv`

## Path Resolution
```python
from modules.common.properties import get_repo_local, get_screenshots_location

repo_root = get_repo_local()
screenshots_dir = get_screenshots_location()
```

- **Never hardcode paths** — always go through `modules/common/properties.py`
- Every path-returning property is routed through that module's `_expand_path()`, which expands
  `$HOME`/`~` — this keeps `properties.yml` portable across machines and usernames
- **Module execution**: activate `.venv`, then run modules by path
  ```bash
  cd ${repo_local} && source .venv/bin/activate && python -m modules.topic.new --path health/dental
  ```
- **User working directory**: pass `os.getcwd()` when a module needs to operate on the current directory
- **Internal paths**: build from `repo_local`, e.g. `Path(repo_local) / "topics/health/dental"`

## Coding Conventions
- Entry point: `if __name__ == "__main__":` calling `main()`
- Type hints on all function parameters and returns
- Named CLI options only (`@cli.option("--title", ...)`) — never positional arguments
- Raise exceptions early; print errors to stderr
- `snake_case` for functions/variables, `UPPER_CASE` for constants
- Module and function docstrings (PEP 257)
- Emoji-prefixed output for user-facing messages
- Non-zero exit codes on failure via `sys.exit()`
- **Alphabetical ordering** for easier navigation: YAML keys, and Python functions within a module
  (except `__init__`, `main()`, and lifecycle methods, which keep their logical order)

```python
# Good
def calculate_total(...): ...
def format_amount(...): ...
def load_topic(...): ...
def validate_date(...): ...

# Exception — main() stays at the end regardless
def main(...): ...
```

## Configuration Files
### properties.yml
Central configuration at the repo root. Keys: `repo` (local path + remote), `icloud` (optional
Obsidian sync path), `skeleton` (shared-tooling source for `/sync-setup`), `screenshots` (location,
cleanup rules, preserved files). Every absolute path uses `$HOME` instead of a hardcoded username, so
the file stays portable across machines.

Load it via `modules.common.properties` — see `modules/repo/README.md` for the full property list.

### Active state files
Both are git-ignored:

| File | Location | Purpose |
|------|----------|---------|
| `active.yml` | `topics/<path>/` | Tracks the active chat in that topic |
| `active_topic.yml` | repo root | Tracks the currently active topic |

```yaml
conversation_file: chats/20260104_checkup_notes.md
started_at: 2026-01-04T15:00:00
topic_path: health/dental
```

This is what lets you just start talking without re-running `/chat resume` or `/topic switch` every
time.

## Notes
- Commits use the format: `Research session: <description>`
- Obsidian-friendly markdown formatting throughout
- Code references use `file_path:line_number` format
- Screenshots are centralized for easy management and AI viewing — see [`screenshots.md`](screenshots.md)
