"""Template generators for topic file content."""

from pathlib import Path

# Repo-relative — never an absolute machine path (see .github/instructions/screenshots.instructions.md)
_LATEST_SCREENSHOT = "screenshots/latest.png"

# ---------------------------------------------------------------------------
# Private section helpers - keep each small for linter compliance
# ---------------------------------------------------------------------------


def _hub_instructions_section() -> str:
    """Return a section directing agents to read the .github/instructions/ hub."""
    return """## Project-Wide Instructions — Always Read First
Before working in any topic, read these instruction files. They apply to every chat and file across the repo:

- **Markdown style rules**: `.github/instructions/style.instructions.md`
- **Docs file standards (CSV, dates, formatting)**: `.github/instructions/docs.instructions.md`
- **Project overview and workflow**: `.github/instructions/project.instructions.md`
- **Topics and research workflow**: `.github/instructions/topics.instructions.md`

Additional instruction files in `.github/instructions/` cover architecture, commands, modules, tests, and screenshots. Read the relevant one when working in those areas."""


def _read_first_section(ancestors: list[tuple[str, str]]) -> str:
    """Return a 'Read First' block listing ancestor OPENCODE.md files.

    Args:
        ancestors: List of (label, path) tuples from root down to immediate parent.
                   e.g. [("Root", "topics/health/OPENCODE.md"),
                          ("Parent", "topics/health/dental/OPENCODE.md")]

    Returns:
        Formatted Read First markdown section.
    """
    lines = [
        "## Read First",
        "Before working in this topic, read the following AGENTS.md files for context:",
        "",
    ]
    for label, path in ancestors:
        lines.append(f"- **{label}**: `{path}`")
    lines.append("")
    return "\n".join(lines)


def _parent_index_section(subtopics: list[tuple[str, str, str]]) -> str:
    """Return the subtopic index section for a parent OPENCODE.md.

    Args:
        subtopics: List of (name, path, description) tuples.

    Returns:
        Formatted subtopic index section.
    """
    lines = [
        "## Subtopics",
        "Each subtopic has its own AGENTS.md with detailed instructions.",
        "Read the relevant child AGENTS.md before working in that subtopic.",
        "",
    ]
    for name, path, description in subtopics:
        lines.append(f"### {name}")
        lines.append(f"**Path**: `{path}`")
        lines.append(f"**Purpose**: {description}")
        lines.append("")
    return "\n".join(lines)


def _screenshot_section() -> str:
    """Return the Screenshots Workflow section."""
    return f"""## Screenshots Workflow
When user types `ss` or `/ss` to view a screenshot, follow these steps IN ORDER:

### Step 1 - Run the screenshot command
Use `/ss` (alias for `/repo view_screenshot`). It copies the most recent screenshot to `latest.png`.

### Step 2 - Read the copied file
```
{_LATEST_SCREENSHOT}
```
Only read this AFTER step 1 completes successfully.

### Step 3 - Describe what you see
Describe the image content to help with the user's research.

**Common mistake to avoid:**
```
❌ WRONG: Read latest.png directly without running /ss first
✅ RIGHT: Run /ss → THEN read latest.png
```"""


def _slash_command_section(tool_name: str = "OpenCode", command_dir: str = ".opencode/command") -> str:
    """Return the Modifying Slash Commands section.

    Args:
        tool_name: Display name of the AI tool (e.g. "OpenCode", "Claude Code", "your AI tool").
        command_dir: Path to the tool's command directory (e.g. ".opencode/command").
    """
    return f"""## Modifying Slash Commands - CRITICAL WORKFLOW
**IMPORTANT:** {tool_name} caches command files. After making changes to `{command_dir}/*.md` files, you MUST restart {tool_name} for changes to take effect.

**Workflow for modifying slash commands:**

1. **Make changes** to the command file (e.g., `{command_dir}/chat.md`)
2. **Save the file**
3. **DO NOT TEST YET** - changes won't work until restart
4. **Close {tool_name}** completely (exit the application)
5. **Reopen/Restart {tool_name}** in the same directory
6. **NOW test the command** - changes should be active

**Why this is necessary:**
- {tool_name} loads and caches all command files at startup
- File changes are not hot-reloaded during runtime
- Testing before restart will show old cached behavior
- This applies to ALL command file changes (frontmatter, content, etc.)

**Common mistake:**
```
❌ WRONG: Edit file → Test immediately → Doesn't work → Get confused
✅ RIGHT: Edit file → Close {tool_name} → Reopen → Test → Works!
```"""


def _workflow_section(tool_name: str = "OpenCode") -> str:
    """Return the AI Tool Workflow section.

    Args:
        tool_name: Display name of the AI tool.
    """
    return f"""## {tool_name} Workflow
When working in this topic with {tool_name}:

1. **Starting a chat**: Use `/chat start` to initialize a new research session
   - **AUTO-CLOSE**: Automatically closes any active chat before starting
   - Previous chat is committed with message "Research session: [title]"
2. **Screenshots**: Type "ss" or "/ss" to examine the latest screenshot
   - **STEP 1 - MANDATORY**: Run `/ss` (copies newest file to latest.png)
   - **STEP 2**: Read `{_LATEST_SCREENSHOT}` (only AFTER step 1 - otherwise you get a stale image)
   - **NEVER** read latest.png without running /ss first
3. **Resuming work**: Use `/chat resume` to continue a previous chat
   - **AUTO-CLOSE**: Automatically closes any active chat before resuming
   - Previous chat is committed with message "Research session: [title]"
   - You can pass a pattern (example: `/chat resume home_security_camera_solution`)
4. **Saving work**: Use `/chat end` to save complete chat log and deactivate session
   - **CRITICAL**: AI agent MUST format and append complete chat log to file before calling `/chat end`
   - See `/chat end` workflow below for detailed instructions
   - `/chat end` saves to file but does NOT commit or push - use git commands when ready
5. **Closing session**: Use `/chat end` to save chat log and clear active status
   - Then start new session with `/chat start` to clear context and reset tokens
   - Or commit changes manually when ready (git add/commit/push)

**Note**: `/chat start` and `/chat resume` now automatically close active chats - no need to manually run `/chat end` first."""


def _commands_section(tool_name: str = "OpenCode") -> str:
    """Return the Available Commands section.

    Args:
        tool_name: Display name of the AI tool.
    """
    return f"""## Available Commands
{tool_name} slash commands (routed to Python modules):
- `/chat start` - Start a new chat session (auto-closes active chat)
- `/chat end` - Save complete chat log to file and deactivate session (does not commit/push)
- `/chat resume` - Resume a previous chat (auto-closes active chat)
- `/chat list` - List all chats in this topic
- `/repo pull` - Pull updates from git remote and iCloud
- `/repo push` - Push changes to git remote and iCloud
- `/repo view_screenshot` - Copy latest screenshot to latest.png (alias: `/ss`)"""


def _chat_end_section() -> str:
    """Return the /chat end Workflow section."""
    return """## `/chat end` Workflow - CRITICAL AI AGENT INSTRUCTIONS
When `/chat end` is called, the AI agent MUST follow this exact sequence:

### Step 1: Format the Complete Chat Log
Create a markdown formatted log of the ENTIRE chat from start to finish:

```markdown
## Chat Log

---
**[YYYY-MM-DD HH:MM:SS] User:**
[User's message]

---
**[YYYY-MM-DD HH:MM:SS] Assistant:**
[Assistant's complete response including code blocks, explanations, etc.]

[Continue for ALL messages...]
```

### Step 2: Append to Chat File
- Read the current chat file (from chats/ directory, filename stored in active.yml)
- Use Edit or Write tool to append the formatted chat log
- Preserve ALL formatting: code blocks (```language), bold, lists, etc.
- Include timestamps for every message
- Maintain chronological order

### Step 3: Confirm and Stop
- After updating the file, confirm it is done in a single short response
- **DO NOT** tell the user to "run `/chat end` again" — the user already ran it; fixing the file is sufficient
- The `/chat end` command will automatically re-validate on the next invocation; that is the user's action, not yours
- **NOTE**: Does NOT commit or push changes - use git commands explicitly when ready
- **TIP**: After ending, start a new chat with `/chat start` to clear context and reset tokens

### Chat Log Format Requirements
- Horizontal rules (`---`) between messages for visual separation
- Bold timestamps and speaker labels: `**[timestamp] Speaker:**`
- Preserve code blocks with syntax highlighting
- Include tool outputs and system messages
- Complete context for future reference

### What /chat end Does
1. ✅ Validates that the complete chat log was saved to the chat file
2. ✅ Clears the active.yml file to deactivate the current session
3. ❌ Does NOT commit changes to git (commit manually when ready)
4. ❌ Does NOT push to remote (push manually when ready)"""


def _file_org_section() -> str:
    """Return the File Organization section."""
    return """## File Organization
- **chats/**: Saved AI chat logs with complete chat history (YYYYMMDD_title.md format)
- **docs/**: User-requested summary documents and reference materials
- **AGENTS.md**: Topic instruction source of truth
- **CLAUDE.md**: Thin pointer to the partner AGENTS.md in the same directory

**Path rule**: Treat the active topic folder as the default working root for all user-requested file paths.
- If user asks for `docs/foo.md`, create `topics/<active_topic>/docs/foo.md`
- If user asks for `scripts/blah.sh`, create `topics/<active_topic>/scripts/blah.sh`
- Only write to repo-root paths when the user explicitly says root/repo-level.

**File default location rule**: ANY file the user asks to create goes in `docs/` by default — `.md`, `.csv`, `.txt`, `.json`, `.yml`, or any other type.
- User says "make a domains.csv" → create `topics/<active_topic>/docs/domains.csv`
- User says "create a headlights.md" → create `topics/<active_topic>/docs/headlights.md`
- User says "make a config.json" → create `topics/<active_topic>/docs/config.json`
- **Core distinction**: `docs/` = user-facing files of any type; `chats/` = AI conversation logs only
- Exception: chat files always go in `chats/`, instruction files stay in their defined locations
- Exception: user explicitly specifies a different path → use that path

**Note**: Screenshots are stored centrally at the repo-root `screenshots/` folder, NOT in topic-specific folders.

### Date Format — MANDATORY
- **Filenames**: Use `YYYYMMDD_description.md` (e.g. `20260409_filming_gear.md`)
- **CSV date fields**: Use ISO 8601 `YYYY-MM-DD` (e.g. `2025-05-15`) — see `.github/instructions/docs.instructions.md`
- **NEVER** use MM/DD/YY or MM/DD/YYYY formats in any file

### Research Document Workflow - CRITICAL
**Default: Research stays in the chat file**
- All research and conversation belongs in the active chat: `chats/YYYYMMDD_title.md`
- Chat logs contain the COMPLETE conversation history for AI context later
- **DO NOT automatically create separate research documents**

**Only create docs/ files when user explicitly requests them:**
- User: "create a doc with the summary" → Create in current topic `docs/category/filename.md`
- User: "give me a markdown file..." → Create the requested file in current topic `docs/`
- User: "make a domains.csv" → Create in current topic `docs/domains.csv`
- User: "make a config.json" → Create in current topic `docs/config.json`
- User does NOT ask for a file → Keep everything in chat

**ALL files go in `docs/` — any type: `.md`, `.csv`, `.txt`, `.json`, `.yml`, etc.**

**Purpose of each folder:**
- **chats/**: AI conversation logs only — for AI to read and understand context
- **docs/**: User-facing files of any type — summaries, data, configs, references (when requested)

**Example:**
- ❌ WRONG: Auto-creating `docs/research.md` during conversation
- ❌ WRONG: Creating any file directly in the topic root
- ✅ RIGHT: Keep all research in `chats/20260226_cameras.md` unless user asks for a file
- ✅ RIGHT: When requested, create `docs/domains.csv`, `docs/config.json`, or `docs/home_security/pricing.md`"""


# ---------------------------------------------------------------------------
# Private builder - assembles all sections
# ---------------------------------------------------------------------------


def _build_opencode_md(
    topic_name: str,
    topic_category: str,
    topic_purpose: str,
    topic_type: str,
    ancestors: list[tuple[str, str]] | None = None,
    tool_name: str = "OpenCode",
    command_dir: str = ".opencode/command",
) -> str:
    """
    Build full instruction file content from section helpers.

    Args:
        topic_name: Display name of the topic.
        topic_category: Category the topic belongs to.
        topic_purpose: Purpose/description of the topic.
        topic_type: Type classification (e.g. Research and Documentation).
        ancestors: Optional list of (label, path) tuples for parent OPENCODE.md files.
                   When provided, a 'Read First' block is prepended.
        tool_name: Display name of the AI tool (e.g. "OpenCode", "Claude Code").
        command_dir: Path to the tool's command directory.

    Returns:
        Complete instruction file content string.
    """
    parts = [
        f"# {tool_name} Instructions for {topic_name}",
        f"This file provides {tool_name}-specific guidance when working in this topic directory.",
        "",
        "**Sync Rule**: Update `AGENTS.md` as the topic content source of truth.",
        " `CLAUDE.md` should remain a thin pointer to the partner `AGENTS.md` in the same directory,"
        " and `OPENCODE.md` only needs updates when OpenCode-specific guidance changes.",
        "",
    ]

    # Always inject hub instructions so agents read project-wide rules
    parts.append(_hub_instructions_section())

    # Inject Read First block if ancestor OPENCODE.md files exist
    if ancestors:
        parts.append(_read_first_section(ancestors))

    parts += [
        "## Topic Information",
        f"**Name**: {topic_name}",
        f"**Category**: {topic_category}",
        f"**Type**: {topic_type}",
        f"**Purpose**: {topic_purpose}",
        "",
        "## Agent Guidelines",
        "When assisting with this topic:",
        "",
        "1. **Understand the context**: Review the topic purpose and requirements",
        "2. **Provide relevant help**: Focus on the specific needs of this topic area",
        "3. **Be accurate**: Ensure information is correct and up-to-date",
        "4. **Be practical**: Offer actionable guidance and solutions",
        "5. **Be organized**: Keep work structured and well-documented",
        "",
        "## Working Environment",
        "- This is a research and troubleshooting workspace",
        "- Chat logs and findings are the primary artifacts",
        "- Screenshots provide visual context",
        f"- {tool_name} is the primary interface (works with any AI model: Claude, GPT, Gemini, etc.)",
        "- Git is used for local version control and optional sync across devices via /push",
        "",
        _workflow_section(tool_name),
        "",
        _commands_section(tool_name),
        "",
        _slash_command_section(tool_name, command_dir),
        "",
        _chat_end_section(),
        "",
        _file_org_section(),
        "",
        _screenshot_section(),
        "",
        "## Best Practices",
        "- Keep chats focused on specific topics or problems",
        "- Use descriptive titles when starting chats",
        "- Capture screenshots for visual context",
        "- AI agents save complete chat logs with timestamps when `/chat end` is called",
        "- Commit work frequently with meaningful messages",
        "- Use `/chat end` at end of session to save locally, then `/push` when ready",
        "",
        "## Collaboration",
        f"Work may be done using various AI models in {tool_name} (Claude, GPT, Gemini, etc.)."
        " Maintain consistency and build on previous work when possible.",
        "",
    ]

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def opencode(
    topic_path: str,
    description: str | None = None,
    repo_root: Path | None = None,
) -> str:
    """
    Generate OPENCODE.md content for a leaf topic.

    Replaces the old create_opencode_template function. Used for both
    creating new topics and regenerating existing OPENCODE.md files.

    When repo_root is provided, walks up topic_path looking for existing
    OPENCODE.md files in ancestor directories under topics/. Any found are
    included in a 'Read First' block at the top of the generated file.

    Args:
        topic_path: Relative path to topic from topics/ root (e.g. health/dental).
        description: Optional custom description for the topic.
        repo_root: Optional absolute path to the repo root. When given, enables
                   dynamic ancestor OPENCODE.md detection.

    Returns:
        Formatted OPENCODE.md content string.
    """
    path = Path(topic_path)
    topic_name = path.name.replace("_", " ").title()
    topic_category = str(path.parent).replace("_", " ").title() if path.parent != Path(".") else "General"

    if description:
        topic_purpose = description
        topic_name = description
    else:
        topic_purpose = f"working with {topic_name}"

    # Build ancestor list by walking up from root to immediate parent
    ancestors: list[tuple[str, str]] = []
    if repo_root is not None:
        topics_root = repo_root / "topics"
        # Walk from the top-level segment down to the immediate parent
        ancestor_path = Path()
        parts = path.parts
        for i, part in enumerate(parts[:-1]):  # exclude the leaf itself
            ancestor_path = ancestor_path / part
            candidate = topics_root / ancestor_path / "AGENTS.md"
            if candidate.exists():
                # Label: "Root" for the top-level, otherwise use folder display name
                label = part.replace("_", " ").title() if i > 0 else part.replace("_", " ").title()
                rel_path = f"topics/{ancestor_path}/AGENTS.md"
                ancestors.append((label, rel_path))

    return _build_opencode_md(
        topic_name,
        topic_category,
        topic_purpose,
        "Research and Documentation",
        ancestors or None,
        tool_name="OpenCode",
        command_dir=".opencode/command",
    )


def agents_md(
    topic_path: str,
    description: str | None = None,
    repo_root: Path | None = None,
) -> str:
    """
    Generate AGENTS.md content (tool-neutral) for a leaf topic.

    Produces the same structure as opencode() but with tool-neutral language,
    suitable for OpenCode, GitHub Copilot, Codex, Cursor, and other AI tools
    that read AGENTS.md.

    Args:
        topic_path: Relative path to topic from topics/ root.
        description: Optional custom description for the topic.
        repo_root: Optional absolute path to the repo root.

    Returns:
        Formatted AGENTS.md content string.
    """
    path = Path(topic_path)
    topic_name = path.name.replace("_", " ").title()
    topic_category = str(path.parent).replace("_", " ").title() if path.parent != Path(".") else "General"

    if description:
        topic_purpose = description
        topic_name = description
    else:
        topic_purpose = f"working with {topic_name}"

    ancestors: list[tuple[str, str]] = []
    if repo_root is not None:
        topics_root = repo_root / "topics"
        ancestor_path = Path()
        parts = path.parts
        for i, part in enumerate(parts[:-1]):
            ancestor_path = ancestor_path / part
            candidate = topics_root / ancestor_path / "OPENCODE.md"
            if candidate.exists():
                label = part.replace("_", " ").title() if i > 0 else part.replace("_", " ").title()
                rel_path = f"topics/{ancestor_path}/OPENCODE.md"
                ancestors.append((label, rel_path))

    return _build_opencode_md(
        topic_name,
        topic_category,
        topic_purpose,
        "Research and Documentation",
        ancestors or None,
        tool_name="your AI tool",
        command_dir=".opencode/command",
    )


def claude_md(
    topic_path: str,  # pylint: disable=unused-argument
    description: str | None = None,  # pylint: disable=unused-argument
    repo_root: Path | None = None,  # pylint: disable=unused-argument
) -> str:
    """
    Generate CLAUDE.md pointer content for a leaf topic.

    CLAUDE.md is a thin pointer that directs Claude Code to read AGENTS.md.
    AGENTS.md is the single source of truth — no content is duplicated here.

    Args:
        topic_path: Unused. Kept for API consistency with agents_md().
        description: Unused. Kept for API consistency with agents_md().
        repo_root: Unused. Kept for API consistency with agents_md().

    Returns:
        CLAUDE.md pointer content string.
    """
    return (
        "# Claude Code Instructions\n"
        "See [AGENTS.md](AGENTS.md) in this directory for full instructions.\n\n"
        "`AGENTS.md` is the single source of truth. Always read and update `AGENTS.md` "
        "— do not duplicate content here.\n"
    )


def parent_opencode(
    topic_path: str,
    subtopics: list[tuple[str, str, str]],
    purpose: str,
    repo_root: Path | None = None,
) -> str:
    """
    Generate a lightweight OPENCODE.md for a parent topic folder.

    Parent folders group related subtopics. They don't have chats/ or docs/
    of their own — they exist only to give AI agents orientation about what
    lives below and how to navigate the tree.

    Args:
        topic_path: Relative path from topics/ root (e.g. health).
        subtopics: List of (name, path, description) tuples for each child subtopic.
                   path should be relative to repo root (e.g. topics/health/dental).
        purpose: One-sentence description of what this parent folder covers.
        repo_root: Optional absolute path to repo root for ancestor OPENCODE.md detection.

    Returns:
        Formatted parent OPENCODE.md content string.
    """
    path = Path(topic_path)
    folder_name = path.name.replace("_", " ").title()

    # Build ancestor list (same logic as opencode())
    ancestors: list[tuple[str, str]] = []
    if repo_root is not None:
        topics_root = repo_root / "topics"
        ancestor_path = Path()
        for part in path.parts[:-1]:
            ancestor_path = ancestor_path / part
            candidate = topics_root / ancestor_path / "OPENCODE.md"
            if candidate.exists():
                label = part.replace("_", " ").title()
                rel_path = f"topics/{ancestor_path}/OPENCODE.md"
                ancestors.append((label, rel_path))

    parts: list[str] = [
        f"# {folder_name}",
        f"**Purpose**: {purpose}",
        "",
        "This is a parent topic folder. It contains subtopics, each with their own",
        "`AGENTS.md`, `CLAUDE.md`, `chats/`, and `docs/` directories.",
        "",
        "**Agent instruction**: Read the relevant subtopic AGENTS.md before working",
        "in that area. Do not create files directly in this parent folder.",
        "",
    ]

    if ancestors:
        parts.append(_read_first_section(ancestors))

    parts.append(_parent_index_section(subtopics))

    return "\n".join(parts)
