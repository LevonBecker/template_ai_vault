---
applyTo: "**"
---
# template_ai_assistant Project Instructions

This is a **personal research and documentation workspace**. It is configured as an AI agent project with custom slash commands and Python module automation. Topics cover whatever areas of your life you organize into `topics/` — home, health, shopping, travel, finances, hobbies, and more.

## What This Repo Is

- **Research workspace**: Chat-based research sessions saved as markdown files under `topics/`
- **Multi-tool**: Works with Claude Code (`.claude/commands/`), OpenCode (`.opencode/command/`), and GitHub Copilot (`.github/prompts/`)
- **Python-powered**: Business logic lives in `modules/` — commands are thin wrappers
- **Git-tracked**: All research syncs via git to iCloud for mobile access

## Instruction Files by Domain

For detailed instructions, read the relevant domain file:

- **Topics & research workflow**: `.github/instructions/topics.instructions.md`
- **Python module architecture**: `.github/instructions/modules.instructions.md`
- **Slash command creation**: `.github/instructions/commands.instructions.md`
- **Testing requirements**: `.github/instructions/tests.instructions.md`
- **System architecture & provider hierarchy**: `.github/instructions/arch.instructions.md`
- **Invoke task runner**: `.github/instructions/invoke.instructions.md`
- **Docs file standards (CSV, etc.)**: `.github/instructions/docs.instructions.md`
- **Markdown style standards**: `.github/instructions/style.instructions.md`
- **Screenshots folder rules**: `.github/instructions/screenshots.instructions.md`
- **Travel topic preferences**: `.github/instructions/travel.instructions.md`

## Instruction File Sync Rule

When updating topic instructions, update `AGENTS.md` as the topic content source of truth. `CLAUDE.md` should remain a thin pointer to the partner `AGENTS.md` in the same directory and should not need topic-specific edits. Update `OPENCODE.md` only when OpenCode-specific guidance changes. Topic init (`/topic init`) and update (`/topic update`) generate these files automatically.

## Core Workflow Commands

### Chat Management
- `/chat start [title]` — Initialize new research chat and create markdown file (auto-closes active chat)
- `/chat end` — Save complete chat log and clear active status (fails if overview/log context is missing); does not commit or push
  - **AI RESPONSE RULE**: When `/chat end` fails because the chat file is incomplete, the AI must update the file and then **stop** — confirm it is done, do NOT instruct the user to "run `/chat end` again". The user already ran it; fixing the file is the AI's only job. The user re-runs the command themselves.
- `/chat list [sort]` — List existing chats in current topic with summaries
- `/chat resume [pattern]` — Resume an existing chat from topic directory (auto-closes active chat; pattern supported)

### Topic Management
- `/topic list` — List all available topics in tree format
- `/topic switch <path>` — Switch to specific topic
- `/topic <path>` — Switch to topic (shorthand)
- `/topic update [--dry-run] [--current-only]` — Update OPENCODE.md files
- `/topic init [description]` — Initialize topic structure

### Repository Maintenance
- `/repo pull` — Pull updates from git remote and iCloud Obsidian folder
- `/repo push` — Push changes to git remote and iCloud Obsidian folder
- `/repo cleanup` — Clean up screenshot images from all screenshots directories
- `/repo set_screenshots` — Configure macOS screenshot location
- `/repo view_screenshot` — Copy latest screenshot to latest.png (alias: `/ss`)
- `/push`, `/pull`, `/ss` — Aliases

### Version Management
- `/version` — Check Python + libs, update config files (does NOT install)
- `/version libs` — Check/update only library versions in pyproject.toml
- `/version python` — Check/update only Python version in config files
- `/upgrade` — Execute upgrades (install Python, rebuild .venv, sync dependencies)
- `/upgrade python` — Upgrade only Python and rebuild .venv
- `/upgrade libs` — Upgrade only libraries (uv sync --upgrade)

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

## File Management Rules

- **ALWAYS** work from git-tracked paths (`topics/`, `agents/`)
- **PREFER** editing existing files over creating new ones
- **USE** ISO 8601 date format everywhere:
  - Filenames: `YYYYMMDD_description.md`
  - CSV date fields: `YYYY-MM-DD` (e.g. `2025-05-15`) — see `.github/instructions/docs.instructions.md`
- **NEVER** write files outside the repository path (`$HOME/Development/levonbecker/template_ai_assistant`) without explicit user permission
  - Repository root is defined in `properties.yml` under `repo.local`
  - All file operations must stay within this boundary
  - If user requests a file outside repo, ask for confirmation first
- **PROPERTIES.YML PATH CONVENTION**: Every absolute filesystem path in `properties.yml` (`repo.local`, `skeleton.local`, `icloud.path`, `screenshots.location`, etc.) MUST use `$HOME` instead of a hardcoded username path
  - ✅ `"$HOME/Development/levonbecker/template_ai_assistant"`
  - ❌ `"/Users/yourname/Development/template_ai_assistant"`
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

## Research Document Workflow

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

**RIGHT ✅**:
- Keep research in chat file until user requests a doc
- When requested: `topics/shopping/electronics/docs/home_security/pricing.md`

## Topic Organization

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

See `docs/README.md` and `modules/topic/README.md` for the group-topic vs. single-topic pattern.

## Documentation Standards

- Markdown files follow CommonMark specification
- Code references: `file_path:line_number` format
- Screenshots stored centrally in `screenshots/` at repo root (ALL topics share this folder)
- Git LFS tracks: `*.png`, `*.jpg`, `*.svg`
- Topic instructions: `AGENTS.md` is the topic source of truth, `CLAUDE.md` is a thin pointer to `AGENTS.md`, and `OPENCODE.md` may carry OpenCode-specific guidance when needed

## Working from Any Directory

The repository is designed so you can start any AI tool from:
1. **Repository root**: Full access to all topics and agents
2. **Any topic subdirectory**: Agents work relative to repository structure
3. **Any nested folder**: Commands auto-detect repository root

**Recommendation**: Start at repository root (use `${repo_local}` from `properties.yml`) then navigate as needed.

See `modules/repo/README.md` for configuration details.

## Sync Strategy

### Git Workflow
- Always commit changes after research sessions
- Descriptive commits: `Research session: [description]`
- Auto-push via `/push` command

### Pre-Push Rule — MANDATORY for Claude Code
**Before the user runs `/push`, commit all pending file edits first.** The push module uses a stash→pull→pop workflow. If uncommitted edits exist when `/push` runs, the stash pop can fail and revert files to the remote version, losing all work.

```bash
# Run this before /push whenever you have uncommitted edits:
git add -A && git commit -m "Research session: [description]"
```

Do not wait for the user to run `/push` and then react to a failure — commit proactively after completing file edits.

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
- **`*.py`** — Any Python file (pylint + ruff)
- **`*.yml`** or **`*.yaml`** — Any YAML file (yamllint)
- **`.github/workflows/*.yml`** — GitHub Actions (actionlint + yamllint)

Skip tests for: `*.md`, config files, `*.toml`, `*.json`

### templates.py Change Rule

`modules/topic/templates.py` is the single source of truth for all topic instruction file content. When you modify it:
1. Run fix + test (10/10 required)
2. **Ask the user**: "Should I run `/topic update` to regenerate all topic AGENTS.md files with the new template?"
3. **Check root `AGENTS.md`** — it is hand-maintained and may need manual sync if the change reflects a new policy

### Testing Workflow

```bash
# 1. Auto-fix first (always do this)
uv run --no-sync invoke fix

# 2. Run tests — must get 10/10
uv run --no-sync invoke test
```

Repeat fix + test until 10/10. Only then commit. See `.github/instructions/tests.instructions.md` for full reference.

### Fix Issues — Never Disable Warnings

If linters complain, fix the actual problem. Don't disable warnings.

```python
# ❌ WRONG
except Exception:  # pylint: disable=broad-exception-caught

# ✅ CORRECT
except (ValueError, KeyError) as e:
    cli.echo(f"Error: {e}")
```

If an issue is too complex: explain what the linter says, what you tried, and ask the user before adding any exclusion.

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

```bash
BASE="path/to/topic"
find "$BASE/pdfs" -name "*.pdf" | while read -r pdf; do
  rel="${pdf#$BASE/pdfs/}"
  txt="$BASE/converted/${rel%.pdf}.txt"
  mkdir -p "$(dirname "$txt")"
  pdftotext "$pdf" "$txt"
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
- `pdftotext` + `pdftoppm` — part of `poppler` (`brew install poppler`)
- `tesseract` — (`brew install tesseract`)

Store converted text in `converted/` mirroring the `pdfs/` folder structure.

## Error Handling

- Commands validate directory structure before execution
- Clear error messages with suggested solutions
- Git operations have rollback protection
- Safe file operations with confirmation when destructive
