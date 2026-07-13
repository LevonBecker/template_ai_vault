# Documentation
The top-level [`README.md`](../README.md) covers the basics (topics, chats, repo sync). This guide covers everything else: full setup, the complete command reference, and how the automation is built.

AI-agent-facing rules (what Claude Code / Copilot / Cline should do, file placement conventions, etc.) live in `.github/instructions/` — start at `.github/instructions/project.instructions.md` if you're customizing agent behavior rather than using the repo.

## Setup
### 1. Initial Setup
```bash
./setup.sh
```

This creates the Python virtual environment, installs dependencies, sets up the test automation tasks, and configures repository properties.

### 2. AI Service Authentication
If you're using OpenCode:
1. Open opencode
2. `CTRL+P`
3. Connect Provider (`CTRL+A`)

##### Anthropic
1. Pro/Max account
2. Copy/paste the URL to your browser
3. Copy/paste the auth key back into OpenCode

##### GitHub Copilot
1. GitHub account
2. Copy/paste the URL to your browser
3. Copy/paste the auth key
4. Approve

##### OpenAI (ChatGPT)
1. Plus/Pro account
2. Copy/paste the URL to your browser
3. Copy/paste the auth key back into OpenCode

### 3. Optional — Install AI Model CLI Tools
Only needed if you want an agent to shell out to another model's CLI.

#### Anthropic Claude Code
```bash
brew install --cask claude-code
claude auth login
# or: export ANTHROPIC_API_KEY="your_api_key_here"
```

#### GitHub CLI
```bash
brew install gh
gh auth login
```

#### GitHub Copilot CLI
```bash
brew install copilot-cli
# Authenticate with your GitHub CLI account
```

#### Google Gemini CLI
```bash
brew install gemini-cli
gemini auth login
# or: export GEMINI_API_KEY="your_api_key_here"
```

#### OpenAI Codex CLI
```bash
brew install codex
codex  # then select ChatGPT auth
```

#### Persist API keys
Add to `~/.zshrc` or `~/.bash_profile`, then `source` it:
```bash
export ANTHROPIC_API_KEY="your_api_key_here"
export GEMINI_API_KEY="your_api_key_here"
```

### 4. Verify Setup
```bash
uv run --no-sync python -m modules.topic.list
```

## Repository Structure
```
template_ai_assistant/
├── topics/                                    # Research topics organized hierarchically
│   │
│   ├── travel/                               # Example: single-level topic
│   │   ├── chats/                            # Conversation history
│   │   │   ├── 20260104_setup.md
│   │   │   └── 20260105_tutorial.md
│   │   ├── docs/                             # Documentation and notes
│   │   ├── AGENTS.md                         # AI agent instructions
│   │   └── active.yml                        # Current active conversation
│   │
│   ├── health/                               # Example: multi-level topic hierarchy
│   │   └── dental/                           # Subtopic: Dental
│   │       ├── chats/
│   │       ├── docs/
│   │       ├── AGENTS.md
│   │       └── active.yml
│   │
│   ├── financials/                           # Topic group: budget, income_tax, investments
│   └── shopping/                             # Single topic — docs/apparel, docs/electronics, docs/auto
│
├── screenshots/                               # Centralized screenshot storage (ALL topics)
│   ├── latest.png                            # Latest screenshot for AI viewing
│   └── Screenshot 2026-01-04 at 3.00.09 PM.png
│
├── modules/                                   # Python modules (core logic)
│   ├── chat/                                 # Conversation lifecycle
│   ├── topic/                                # Topic structure
│   ├── repo/                                 # Repository operations
│   └── common/                               # Shared utilities
│
└── .opencode/                                 # AI agent configuration
    └── command/                               # Custom slash commands
```

## Screenshots
- Centralized location: `screenshots/` at repo root (shared by all topics)
- macOS: `Cmd+Shift+4` saves there automatically once configured (`/repo set_screenshots`)
- Type `ss` (or `/repo view_screenshot`) to have the AI view the latest screenshot

## Command Reference
### Chat
| Command | Purpose | Details |
|---------|---------|---------|
| `/chat start [title]` | Create new conversation | Auto-ends active chat, creates `YYYYMMDD_title.md` in `chats/` |
| `/chat resume [pattern]` | Switch to a different conversation | Filters by filename/date/pattern, prompts for selection |
| `/chat list` | List all chats | Shows all chats in the current topic |
| `/chat end` | End conversation | Writes the full log to the chat file, clears active status |

### Topic
| Command | Purpose | Details |
|---------|---------|---------|
| `/topic list` | Show active topic | |
| `/topic list all` | Show full topic tree | Marks the active topic |
| `/topic switch <path>` / `/topic <path>` | Switch to a topic | Auto-saves current chat, switches context, resumes active chat |
| `/topic new <path> [description]` | Create + initialize a new topic | |
| `/topic init [description]` | Initialize the current directory as a topic | |
| `/topic update [--dry-run]` | Regenerate AGENTS.md/CLAUDE.md files | Rolls out template changes across all topics |

### Repo & Screenshots
| Command | Purpose | Details |
|---------|---------|---------|
| `/push` | Push changes | Runs `invoke fix` + `invoke test`, then commits and pushes |
| `/pull` | Pull updates | Stashes local changes, pulls with rebase, restores stash |
| `/repo cleanup` | Remove old screenshots | Deletes all screenshots except `latest.png` |
| `/repo set_screenshots` | Configure screenshot location | Sets macOS to save screenshots to the central folder |
| `/ss` / `/repo view_screenshot` | View latest screenshot | Copies latest screenshot to `latest.png` and reads it |

## Agent Automation Architecture
### Command → Script Mapping
All commands are thin wrappers that call Python modules directly:

**Chat Manager** (`modules/chat/`)
- `/chat start` / `/chat list` / `/chat resume` / `/chat end` → `modules/chat/route.py`

**Topic Manager** (`modules/topic/`)
- `/topic list` / `/topic switch` / `/topic new` / `/topic init` / `/topic update` → `modules/topic/route.py`

**Repository Manager** (`modules/repo/`)
- `/push`, `/pull`, `/repo cleanup`, `/repo set_screenshots`, `/repo view_screenshot` (alias `/ss`) → `modules/repo/route.py`

### Python Modules
```
modules/
├── chat/                        # Chat lifecycle
│   ├── active.py                # Active chat state (active.yml)
│   ├── route.py                 # /chat routing
│   ├── start.py
│   ├── end.py
│   ├── list.py
│   ├── resume.py
│   └── README.md
├── topic/                       # Topic structure management
│   ├── active.py                # Active topic state (active_topic.yml)
│   ├── route.py                 # /topic routing
│   ├── new.py
│   ├── init.py
│   ├── list.py
│   ├── switch.py
│   ├── templates.py             # AGENTS.md/OPENCODE.md content templates
│   ├── update.py
│   └── README.md
├── repo/                        # Repository operations
│   ├── cleanup.py
│   ├── push.py
│   ├── pull.py
│   ├── set_screenshots.py
│   ├── view_screenshot.py       # /repo view_screenshot
│   ├── route.py                 # /repo routing
│   └── README.md
└── common/                      # Shared utilities
    ├── properties.py            # Central properties loader
    ├── utils.py
    └── README.md
```

### Design Principles
1. **Commands are thin wrappers** — all logic lives in Python modules under `modules/`
2. **Python modules do the work** — validation, business logic, error handling
3. **Invoke tasks for CI** — `tasks/` drives tests and automation
4. **Composable & testable** — modules can be tested independently
5. **No side effects outside the repo** — only read/write git-tracked paths
6. **Clear error messages** — emoji prefixes: ✅ ❌ ⚠️ 📂 🎯
7. **Virtual environment** — all Python commands require `.venv`

### Testing Commands Directly
All automation can be run without slash commands:

```bash
cd $HOME/Development/levonbecker/template_ai_assistant
source .venv/bin/activate

# Chat management
uv run python -m modules.chat.start --title="test title"
uv run python -m modules.chat.list
uv run python -m modules.chat.resume --pattern="pattern"

# Topic management
uv run python -m modules.topic.list
uv run python -m modules.topic.new --path health/dental

# Repository management
uv run python -m modules.repo.cleanup
uv run python -m modules.repo.pull
uv run python -m modules.repo.push
uv run python -m modules.repo.set_screenshots
uv run python -m modules.repo.view_screenshot
```

Repository paths are managed centrally via `properties.yml` — see `modules/repo/README.md` and `modules/common/README.md`.

### Creating New Commands
1. Create the Python module: `modules/{manager}/{name}.py`
2. Add an invoke task if needed: update `tasks/`
3. Test the module directly with real inputs
4. Create the source-of-truth prompt: `.github/prompts/{name}.prompt.md`
5. Sync it to the other tools: `inv claude.sync`, `inv cline.sync`, `inv opencode.sync`
6. Update the manager's `README.md`

See `.github/instructions/commands.instructions.md` for the full convention.

### Python Module Standards
- Entry point: `if __name__ == "__main__":` calling `main()`
- Type hints on all function parameters and returns
- Raise exceptions early; print errors to stderr
- `snake_case` for functions/variables, `UPPER_CASE` for constants
- Module and function docstrings (PEP 257)
- Emoji-prefixed output for user-facing messages
- Non-zero exit codes on failure via `sys.exit()`

### Coding Conventions
**Alphabetical ordering**, for easier navigation:
- YAML files: keys ordered alphabetically (e.g. `properties.yml`)
- Python functions: alphabetical within a module, except `__init__`, `main()`, and lifecycle methods, which keep their logical order

```python
# Good
def calculate_total(...): ...
def format_amount(...): ...
def load_topic(...): ...
def validate_date(...): ...

# Exception — main() stays at the end regardless
def main(...): ...
```

### Path Resolution Pattern
```python
from modules.common.properties import get_properties

properties = get_properties()
repo_local = properties["repo"]["local"]
```

- **Module execution**: activate `.venv`, then run modules by path
  ```bash
  cd ${repo_local} && source .venv/bin/activate && python -m modules.topic.new --path health/dental
  ```
- **User working directory**: pass `os.getcwd()` when a module needs to operate on the current directory
- **Internal paths**: build from `repo_local`, e.g. `Path(repo_local) / "topics/health/dental"`

Every path-returning property is routed through `modules/common/properties.py`'s `_expand_path()`, which expands `$HOME`/`~` — this keeps `properties.yml` portable across machines and usernames.

## Configuration Files
### properties.yml
Central configuration at the repo root. Keys: `repo` (local path + remote), `icloud` (optional Obsidian sync path), `skeleton` (shared-tooling source for `/sync-setup`), `screenshots` (location, cleanup rules, preserved files).

Load it via `modules.common.properties.get_properties()` — see `modules/repo/README.md` for the full property list.

### Active state files
- `active.yml` (per-topic) — tracks the active chat in that topic
- `active_topic.yml` (repo root) — tracks the currently active topic

```yaml
conversation_file: chats/20260104_checkup_notes.md
started_at: 2026-01-04T15:00:00
topic_path: health/dental
```

This is what lets you just start talking without re-running `/chat resume` or `/topic switch` every time.

## Notes
- Commits use the format: `Research session: <description>`
- Obsidian-friendly markdown formatting throughout
- Code references use `file_path:line_number` format
- Screenshots are centralized for easy management and AI viewing
