# AI Agent Instructions - template_ai_assistant Repository
## Project-Wide Instructions — Always Read First
Before working in any topic, read these instruction files from `.github/instructions/`. They apply to every chat and file in the repo:

- **Markdown style rules**: `.github/instructions/style.instructions.md`
- **Docs file standards (CSV, dates, formatting)**: `.github/instructions/docs.instructions.md`
- **Project overview and workflow**: `.github/instructions/project.instructions.md`
- **Topics and research workflow**: `.github/instructions/topics.instructions.md`

Additional files in `.github/instructions/` cover architecture, commands, modules, tests, and screenshots. Read the relevant one when working in those areas.

## Repository Context
This is a **personal research and documentation workspace**, configured as an **AI agent project** with custom slash commands and agent automation. Designed for any research topic you want to track — home, health, shopping, travel, finances, hobbies, and more.

## Core Workflow Agents
The following agents are available from **any directory** in the repository:

### Chat Management
- `/chat start [title]` - Initialize new research chat and create markdown file (auto-closes active chat)
- `/chat end` - Save complete chat log and clear active status (fails if overview/log context is missing); does not commit or push
  - **AI RESPONSE RULE**: When `/chat end` fails because the chat file is incomplete, the AI must update the file and then **stop** — confirm it is done, do NOT instruct the user to "run `/chat end` again". The user already ran it; fixing the file is the AI's only job. The user re-runs the command themselves.
- `/chat list [sort]` - List existing chats in current topic with summaries
- `/chat resume [pattern]` - Resume an existing chat from topic directory (auto-closes active chat; pattern supported)

### Topic Management
- `/topic list` - List all available topics in tree format
- `/topic switch <path>` - Switch to specific topic
- `/topic <path>` - Switch to topic (shorthand)
- `/topic update [--dry-run] [--current-only]` - Update OPENCODE.md files
- `/topic init [description]` - Initialize topic structure

### AI Tool Sync
Run after adding or modifying any `.github/prompts/*.prompt.md` file. `.github/prompts/` is the source of truth.
- `inv ai.sync` - Sync all AI tools at once (claude + cline + hermes + opencode)
- `inv claude.sync` - Sync `.claude/commands/`
- `inv cline.sync` - Sync `.clinerules/workflows/`
- `inv hermes.sync` - Sync `~/.hermes/` config + SKILL.md
- `inv opencode.sync` - Sync `.opencode/command/`

### Ollama (Local LLM)
- `inv ollama.install` - Install Ollama + local coding LLM on Apple Silicon
- `inv ollama.list` - List installed and available models
- `inv ollama.status` - Show Ollama service and running-model status
- `inv ollama.update` - Update Ollama binary + all installed models
- `inv ollama.clean` - Remove all downloaded models and blob cache
- `inv ollama.start` / `inv ollama.stop` / `inv ollama.restart` - Service control
- `inv ollama.uninstall` - Uninstall Ollama + remove all models

### Repository Maintenance
- `/repo pull` - Pull updates from git remote and iCloud Obsidian folder
- `/repo push` - Push changes to git remote and iCloud Obsidian folder
- `/repo cleanup` - Clean up screenshot images from all screenshots directories
- `/repo set_screenshots` - Configure macOS screenshot location
- `/repo view_screenshot` - Copy latest screenshot to latest.png (alias: `/ss`)
- `/push`, `/pull`, `/ss` - Aliases

### Version Management
- `/version` - Check Python + libs, update config files (does NOT install)
- `/version libs` - Check/update only library versions in pyproject.toml
- `/version python` - Check/update only Python version in config files
- `/upgrade` - Execute upgrades (install Python, rebuild .venv, sync dependencies)
- `/upgrade python` - Upgrade only Python and rebuild .venv
- `/upgrade libs` - Upgrade only libraries (uv sync --upgrade)

**Workflow**: Run `/version` to review and update configs → check `git diff` → run `/upgrade` to install

## Important Conventions
### uv run --no-sync
All slash commands that use `uv run` MUST include the `--no-sync` flag to prevent automatic dependency synchronization on every command execution.

```bash
# ✅ Correct:
uv run --no-sync python -m modules.topic.route "$ARGUMENTS"
uv run --no-sync invoke test

# ❌ Incorrect (will sync deps unnecessarily):
uv run python -m modules.topic.route "$ARGUMENTS"
uv run invoke test
```

**Why this matters:**
- ⚡ Faster command execution (no sync overhead)
- 🎯 Predictable environment state
- 🔧 Explicit control over when dependencies sync

**When to sync:**
Use `/upgrade` or `uv run --no-sync invoke upgrade.sync` when you intentionally want to sync dependencies.

## Agent Structure
**CRITICAL: Commands are thin wrappers. Logic lives in Python modules.**

### Architecture Layers (MANDATORY PATTERN)
```
User → AI Tool Slash Command → Router Module → Python Module
        (tool command dir)       (modules/*)     (modules/)
```

Tool command dirs: `.opencode/command/` (OpenCode), `.claude/commands/` (Claude Code), `.github/prompts/` (Copilot)

**Layer 1: Slash Commands** (`.opencode/command/*.md`, `.claude/commands/*.md`, `.github/prompts/*.prompt.md`)
- Thin wrappers that call router modules
- NO business logic or bash work here
- Example: `/chat resume wire_tunnels` → calls `uv run python -m modules.chat.route "resume wire_tunnels"`

**Layer 2: Router Modules** (`modules/*/route.py`)
- Parse arguments and dispatch to the target module
- Runs the Python module directly

**Layer 3: Python Modules** (`modules/*/`)
- ALL business logic lives here
- All actual work happens here
- Reusable, testable, documented
- Example: `modules/chat/resume.py` does the actual chat resuming

**Why this matters:**
1. ✅ Commands work in OpenCode AND from terminal
2. ✅ Logic is testable and maintainable
3. ✅ No duplication between OpenCode and CLI usage
4. ✅ Clear separation of concerns
5. ✅ Future AI agents can call same functionality

### Module Organization
All modules are located in `/modules/` directory organized by responsibility:

```
modules/
├── chat/          # Chat lifecycle operations
├── claude/        # Claude Code integration (route, sync)
├── cline/         # Cline integration (sync)
├── hermes/        # Hermes AI agent integration (sync)
├── ollama/        # Local LLM setup on Apple Silicon
├── opencode/      # OpenCode integration (sync)
├── repo/          # Repository maintenance tasks
├── topic/         # Topic navigation and setup
└── common/        # Shared utilities
```

Each module contains:
- `*.py` - Python modules with all business logic
- `README.md` - Complete documentation and usage

**See `.github/instructions/arch.instructions.md` for complete details.**

### Python Module CLI Standards - MANDATORY
**CRITICAL RULE: All Python modules MUST use named options (`@cli.option`), NOT positional arguments.**

This is a repository-wide architectural standard for consistency and maintainability.

#### ✅ CORRECT - Named Options (Property Style)
```python
from modules.common import cli

@cli.command()
@cli.option("--title", default=None, help="Title for the chat")
@cli.option("--pattern", default=None, help="Search pattern")
def main(title: str | None = None, pattern: str | None = None):
    """Your module logic."""
    pass
```

**Usage:**
```bash
uv run --no-sync python -m modules.chat.start --title="my chat"
/chat start my chat  # OpenCode routes via modules/chat/route.py
```

**Why named options:**
- Self-documenting (clear what each parameter does)
- Order-independent (can specify in any order)
- Professional (industry standard for Python CLIs)
- Maintainable (easy to add new options)
- Pythonic (follows community best practices)
- OpenCode compatible (works seamlessly with slash commands)

#### ❌ WRONG - Positional Arguments
```python
def main(title, pattern):
    pass
```

**Why positional is wrong:**
- Not self-documenting (unclear what position means)
- Order-dependent (must remember sequence)
- Error-prone (easy to mix up parameters)
- Not Pythonic (Python prefers named parameters)

#### Common Patterns
```python
# Optional parameter
@cli.option("--title", default=None, help="Title for the chat")

# Required parameter
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

#### What CLI Helper Provides
`modules.common.cli` provides a small TUI-safe command-line interface layer:

- **Automatic parsing** - Converts CLI strings to Python types
- **Help generation** - Auto-generates `--help` documentation
- **Type validation** - Ensures correct types (string, int, bool, Path)
- **Default values** - Handles optional parameters elegantly
- **Interactive prompts** - Can prompt for missing required values
- **Error handling** - User-friendly error messages
- **Professional UX** - Industry-standard CLI patterns

#### AI Tool Integration
The router architecture works seamlessly with named options:

```
User: /chat start my chat
  ↓
AI tool: runs command file (e.g., .opencode/command/chat.md)
  ↓
Command file executes: uv run python -m modules.chat.route "start my chat"
  ↓
Router module dispatches: modules.chat.start --title="my chat"
  ↓
Click Module: Parses --title parameter
  ↓
Python Function: Receives title="my chat"
```

#### Fetching Repository Paths
Modules must use `modules/repo/fetch_properties.py` for paths:

```python
from ..repo.fetch_properties import get_repo_local, get_expense_csv_path

# Get repo root
repo_root = get_repo_local()

# Get expense CSV for current year
expense_csv = get_expense_csv_path(2026)

# Get screenshots location
screenshots = get_screenshots_location()
```

**Never hardcode paths.** Always use centralized property fetching.

**See `.github/instructions/commands.instructions.md` and `.github/instructions/modules.instructions.md` for complete module creation workflow.**

## How Slash Commands Work
Slash commands are executed via router modules embedded in the command file.

1. OpenCode reads the corresponding `.opencode/command/*.md` file
2. The file runs a router module using `!` command injection
3. The router parses `$ARGUMENTS` and runs the target module

**Example (OpenCode):**
```
User types: /chat resume wire_tunnels
Command file: .opencode/command/chat.md
Command executes: uv run python -m modules.chat.route "resume wire_tunnels"
Router runs: modules.chat.resume --pattern="wire_tunnels"
```

### Creating New Slash Commands - REQUIRED SETUP
**CRITICAL ARCHITECTURE RULE: Commands MUST be thin wrappers that call router modules.**

#### Step 1: Create Python Module (modules/)
**ALL business logic goes here. NO exceptions.**

```python
# modules/your_module/your_task.py
"""Your task description."""
from modules.common import cli

@cli.command()
@cli.option("--argument", required=False, help="Description")
def main(argument: str | None = None) -> None:
    """
    Your task logic here.

    This is where ALL the work happens:
    - File operations
    - Git commands
    - Data processing
    - Everything
    """
    # Do the actual work here
    cli.echo(f"Processing: {argument}")
```

#### Step 2: Create Router Module (modules/)
**Thin router that dispatches to the Python module.**

```python
# modules/your_module/route.py
import shlex
import subprocess
import sys

from modules.common.route_utils import build_env, find_repo_root


def main() -> int:
    raw_args = sys.argv[1] if len(sys.argv) > 1 else ""
    args = shlex.split(raw_args)
    repo_root = find_repo_root()
    env = build_env(repo_root)
    cmd = [sys.executable, "-m", "modules.your_module.your_task", *args]
    return subprocess.run(cmd, cwd=repo_root, env=env, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
```

#### Step 3: Create Slash Command (.opencode/command/, .claude/commands/, .github/prompts/)
**Thin wrapper that runs the router.**

**Required frontmatter:**
```yaml
---
description: Brief description of what the command does
agent: general
subtask: false  # CRITICAL - prevents Task tool recursion
slash_command: /your_command
---
```

**Required content:**
```markdown
!`uv run python -m modules.your_module.route "$ARGUMENTS"`
```

**Why this architecture:**
1. ✅ Same command works in OpenCode AND terminal (`uv run python -m modules.your_module.route "args"`)
2. ✅ All logic is testable (Python modules)
3. ✅ No duplication between OpenCode and CLI
4. ✅ Slash commands are just thin wrappers

**DO NOT:**
- ❌ Put business logic in slash command markdown files
- ❌ Write bash scripts directly in slash commands
- ❌ Use `subtask: true` (causes Task tool recursion)

**See `.github/instructions/commands.instructions.md` for complete documentation.**

### Modifying Slash Commands - CRITICAL WORKFLOW
**IMPORTANT:** AI tools cache command files. After making changes to command files, you MUST restart your AI tool for changes to take effect.

**Workflow for modifying slash commands:**

1. **Make changes** to the command file (e.g., `.opencode/command/resume.md`, `.claude/commands/resume.md`)
2. **Save the file**
3. **DO NOT TEST YET** - changes won't work until restart
4. **Close/restart your AI tool** completely
5. **Reopen your AI tool** in the same directory
6. **NOW test the command** - changes should be active

**Why this is necessary:**
- AI tools load and cache all command files at startup
- File changes are not hot-reloaded during runtime
- Testing before restart will show old cached behavior
- This applies to ALL command file changes (frontmatter, content, etc.)

**Common mistake:**
```
❌ WRONG: Edit file → Test immediately → Doesn't work → Get confused
✅ RIGHT: Edit file → Restart your AI tool → Test → Works!
```

## Key Principles
### Instruction File Sync Rule
**When updating topic instructions, update `AGENTS.md` as the topic content source of truth.** `CLAUDE.md` should remain a thin pointer to the partner `AGENTS.md` in the same directory and should not need topic-specific edits. Update `OPENCODE.md` only when OpenCode-specific guidance changes. Topic init (`/topic init`) and update (`/topic update`) generate these files automatically.

### File Management
- **ALWAYS** work from git-tracked paths (`topics/`, `agents/`)
- **PREFER** editing existing files over creating new ones
- **USE** ISO 8601 date format everywhere:
  - Filenames: `YYYYMMDD_description.md`
  - CSV date fields: `YYYY-MM-DD` (e.g. `2025-05-15`) — see `.github/instructions/docs.instructions.md`
- **CREDIT CARDS CSV RULE**: When editing `topics/financials/budget/docs/credit_cards.csv`, always recalculate:
  - `available_credit` for every card affected by balance/limit changes
  - `TOTAL` row fields for `balance`, `credit_limit`, and `available_credit`
- **NEVER** write files outside the repository path (`$HOME/Development/levonbecker/template_ai_assistant`) without explicit user permission
  - Repository root is defined in `properties.yml` under `repo.local`
  - All file operations must stay within this boundary
  - If user requests a file outside repo, ask for confirmation first
- **PROPERTIES.YML PATH CONVENTION**: Every absolute filesystem path in `properties.yml` (`repo.local`, `skeleton.local`, `icloud.path`, `screenshots.location`, etc.) MUST use `$HOME` instead of a hardcoded username path
  - ✅ `"$HOME/Development/levonbecker/template_ai_assistant"`
  - ❌ `"$HOME/Development/levonbecker/template_ai_assistant"`
  - `modules/common/properties.py` expands `$HOME` and `~` via `_expand_path()` before returning any `Path` — always route new path-returning properties through that helper
  - This keeps `properties.yml` portable across machines/usernames; only update the helper if a new path format is introduced
- **DEFAULT PATH RULE**: Treat the active topic as the root for user-requested relative paths
  - `docs/...` means `{active_topic_path}/docs/...`
  - `scripts/...` means `{active_topic_path}/scripts/...`
  - Any relative path defaults to `{active_topic_path}/...` unless user explicitly requests repo root
- **FILE DEFAULT LOCATION RULE**: Any file the user asks to create goes in `{active_topic_path}/docs/` by default — `.md`, `.csv`, `.txt`, `.json`, `.yml`, or any other type
  - User says "make a domains.csv" → create `{active_topic_path}/docs/domains.csv`
  - User says "create a headlights.md" → create `{active_topic_path}/docs/headlights.md`
  - User says "make a config.json" → create `{active_topic_path}/docs/config.json`
  - **Core distinction**: `docs/` = user-facing files of any type; `chats/` = AI conversation logs only
  - Exception: chat files always go in `chats/`, instruction files stay in their defined locations
  - Exception: user explicitly specifies a different path → use that path

### Research Document Workflow - CRITICAL
**Default behavior: Research stays in the chat file**
- All research, conversation, and findings belong in the active chat file (`chats/YYYYMMDD_title.md`)
- **DO NOT automatically create separate research documents**
- Chat files contain the complete conversation history

**Only create docs/ files when explicitly requested:**
- User says: "create a doc with the pricing summary" → Create `docs/category/pricing.md`
- User says: "give me a markdown file with..." → Create the requested file in `docs/`
- User says: "make a domains.csv" → Create `docs/domains.csv`
- User does NOT ask for a file → Keep everything in the chat file

**File location when requested:**
- **ALWAYS in active topic's `docs/` folder**: `{active_topic_path}/docs/{filename}` or `{active_topic_path}/docs/{category}/{filename}`
- This applies to **all file types** — `.md`, `.csv`, `.txt`, `.json`, `.yml`, etc.
- **Core distinction**: `docs/` = user-facing files of any type; `chats/` = AI conversation logs only
- **Active topic path** tracked in `active_topic.yml` (e.g., `topics/shopping/electronics`)
- **Example**: `topics/shopping/electronics/docs/home_security/unifi_pricing.md`
- **Example**: `topics/food_and_drink/docs/recipes/favorite_chili.md`
- **Example**: `topics/home/docs/network/router_config.json`

**WRONG ❌**:
- Auto-creating research docs without being asked
- Creating files in repo root: `$HOME/Development/levonbecker/template_ai_assistant/research.md`
- Creating any file directly in the topic root instead of `docs/`

**RIGHT ✅**:
- Keep research in chat file until user requests a file
- When requested: `topics/shopping/electronics/docs/home_security/pricing.md`
- When requested: `topics/food_and_drink/docs/recipes/favorite_chili.md`

### Topic Organization
```
topics/
├── health/           # Group topic — dental, fitness, medical, supplements, vision
├── travel/           # Single topic — docs/ split by category (trips, documentation, packing)
├── home/             # Single topic — docs/ split by category (security, network, appliances)
├── financials/       # Group topic — budget, income_tax, investments
├── shopping/         # Single topic — docs/ split by category (apparel, electronics, auto)
├── help/             # Group topic — macos, linux, online, projects
└── food_and_drink/   # Single topic — docs/ split by category (appliances, favorites, recipes)
```

### Documentation Standards
- Markdown files follow CommonMark specification
- Code references: `file_path:line_number` format
- Screenshots stored centrally in `screenshots/` at repo root (ALL topics share this folder)
- Git LFS tracks: `*.png`, `*.jpg`, `*.svg`
- Topic instructions: `AGENTS.md` is the topic source of truth, `CLAUDE.md` is a thin pointer to `AGENTS.md`, and `OPENCODE.md` may carry OpenCode-specific guidance when needed

## Working from Any Directory
The repository is designed so you can start OpenCode from:
1. **Repository root**: Full access to all topics and agents
2. **Any topic subdirectory**: Agents work relative to repository structure
3. **Any nested folder**: Commands auto-detect repository root

**Recommendation**: Start your AI tool at repository root (use `${repo_local}` from properties.yml) then navigate to topic folders as needed.

See `modules/repo/README.md` for configuration details.

## Sync Strategy
### Git Workflow
- Always commit changes after research sessions
- Descriptive commits: `Research session: [description]`
- Auto-push via `/push` command

### iCloud Integration
- Repository syncs to iCloud Obsidian vault (content only, no .git/)
- Mobile access to markdown files and documentation
- 700KB lean sync (excludes hidden files and git history)

### Multi-Device Continuity
- Full git repo on Mac with all tools and history
- Lightweight markdown vault on iOS for reference
- Seamless pickup of research across devices

## Code Quality Requirements
**🌟 MANDATORY: Changes to Python or YAML files MUST pass tests with 10/10 score 🌟**

### When to Run Tests
Run tests if you modify:
- **`*.py`** - Any Python file (checked by pylint + ruff)
- **`*.yml`** or **`*.yaml`** - Any YAML file (checked by yamllint)
- **`.github/workflows/*.yml`** - GitHub Actions (checked by actionlint + yamllint)

Skip tests for:
- Markdown files (`*.md`)
- Git/editor config files
- Other non-Python/YAML files

### templates.py Change Rule
`modules/topic/templates.py` is the single source of truth for all topic instruction file content. When you modify it:
1. Run fix + test (10/10 required)
2. **Ask the user**: "Should I run `/topic update` to regenerate all topic AGENTS.md files with the new template?"
3. **Check root `AGENTS.md`** — it is hand-maintained and may need manual sync if the change reflects a new policy

### Testing Workflow
Whenever you modify Python or YAML files:

1. **Auto-fix FIRST (always do this):**
   ```bash
  uv run --no-sync invoke fix
   ```
   This auto-fixes most issues (formatting, import sorting, etc.)

2. **Run tests:**
   ```bash
  uv run --no-sync invoke test
   ```

3. **Required result:** 10/10 score with exit code 0

4. **If tests fail, manually fix** remaining issues (type hints, unused imports, etc.)

5. **Repeat fix + test until 10/10:**
   ```bash
  uv run --no-sync invoke fix
  uv run --no-sync invoke test
   ```

6. **Only then commit** your changes

### What Gets Tested
- ✅ actionlint - GitHub Actions workflow validation
- ✅ pylint - Python code quality checking
- ✅ ruff - Python linting and formatting
- ✅ yamllint - YAML file validation

**See `.github/instructions/tests.instructions.md` for complete testing documentation.**

### The Golden Rule
**IF YOU CHANGE `.py`, `.yml`, or `.yaml` FILES, YOU MUST GET 10/10 ON TESTS.**

No exceptions. No shortcuts. No "I'll fix it later." Quality code is non-negotiable.

### Fix Issues, Don't Disable Warnings
**CRITICAL PHILOSOPHY: If linters complain, fix the actual problem. Don't disable warnings.**

**❌ NEVER DO THIS (without asking first):**
```python
except Exception:  # pylint: disable=broad-exception-caught
```

**✅ ALWAYS DO THIS:**
```python
except (ValueError, KeyError) as e:
    cli.echo(f"Error: {e}")
```

**Why:**
- Linters catch real problems (broad exceptions, missing types, etc.)
- Disabling warnings hides issues instead of fixing them
- We want high-quality, maintainable code
- If you can't figure out the specific exception, catch multiple specific ones

**If Issue Is Really Complex:**

1. **Try to fix it properly first** - Spend reasonable effort
2. **If stuck, ASK THE USER:**
   - Explain what the linter is complaining about
   - Show what you've tried
   - Ask: "This is complicated to fix properly. Should I add an exclusion or keep trying?"
3. **Wait for user approval** before adding any exclusions

See `.github/instructions/tests.instructions.md` for examples of proper exception handling and when to ask.

## Reading PDF Files
When a user wants you to read PDFs (documents, reports, scans, invoices, etc.), use this two-pass workflow:

### Step 1: Try pdftotext (fast — works on text-based PDFs)
```bash
pdftotext "path/to/file.pdf" "path/to/output.txt"
```

Check if the output has content (`wc -l < output.txt` > 1). If yes, read it directly.

### Step 2: OCR with pdftoppm + tesseract (for scanned/image-based PDFs)
If pdftotext produced an empty or near-empty file, the PDF is image-based. Use OCR:

```bash
# Render each page to PNG at 300dpi
pdftoppm -r 300 -png "input.pdf" /tmp/pages/page

# OCR each page and concatenate
for img in /tmp/pages/page-*.png; do
  tesseract "$img" stdout -l eng 2>/dev/null >> output.txt
done
```

### Batch Workflow (mirror folder structure)
To convert an entire directory of PDFs:

```bash
BASE="path/to/topic"
find "$BASE/pdfs" -name "*.pdf" | while read -r pdf; do
  rel="${pdf#$BASE/pdfs/}"
  txt="$BASE/converted/${rel%.pdf}.txt"
  mkdir -p "$(dirname "$txt")"

  # Pass 1: pdftotext
  pdftotext "$pdf" "$txt"

  # Pass 2: OCR if empty
  if [ "$(wc -l < "$txt")" -le 1 ]; then
    PAGES=$(mktemp -d)
    pdftoppm -r 300 -png "$pdf" "$PAGES/page"
    > "$txt"
    for img in "$PAGES"/page-*.png; do
      [ -f "$img" ] && tesseract "$img" stdout -l eng 2>/dev/null >> "$txt"
    done
    rm -rf "$PAGES"
  fi
done
```

### Requirements
Both tools are installed via Homebrew:
- `pdftotext` — part of `poppler` (`brew install poppler`)
- `tesseract` — (`brew install tesseract`)
- `pdftoppm` — part of `poppler` (same install)

### Notes
- Store converted text in `converted/` mirroring the `pdfs/` folder structure
- Always try pdftotext first — it's faster and more accurate for text-based PDFs
- OCR quality depends on scan resolution; 300dpi is the minimum recommended
- Some PDFs (arm bands, barcodes) will produce garbled output — that is expected

## Error Handling
- Commands validate directory structure before execution
- Clear error messages with suggested solutions
- Git operations have rollback protection
- Safe file operations with confirmation when destructive
