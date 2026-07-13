# your AI tool Instructions for Budget
This file provides your AI tool-specific guidance when working in this topic directory.

**Sync Rule**: Update `AGENTS.md` as the topic content source of truth.
 `CLAUDE.md` should remain a thin pointer to the partner `AGENTS.md` in the same directory, and `OPENCODE.md` only needs updates when OpenCode-specific guidance changes.

## Project-Wide Instructions — Always Read First
Before working in any topic, read these instruction files. They apply to every chat and file across the repo:

- **Markdown style rules**: `.github/instructions/style.instructions.md`
- **Docs file standards (CSV, dates, formatting)**: `.github/instructions/docs.instructions.md`
- **Project overview and workflow**: `.github/instructions/project.instructions.md`
- **Topics and research workflow**: `.github/instructions/topics.instructions.md`

Additional instruction files in `.github/instructions/` cover architecture, commands, modules, tests, and screenshots. Read the relevant one when working in those areas.
## Topic Information
**Name**: Budget
**Category**: Financials
**Type**: Research and Documentation
**Purpose**: working with Budget

## Agent Guidelines
When assisting with this topic:

1. **Understand the context**: Review the topic purpose and requirements
2. **Provide relevant help**: Focus on the specific needs of this topic area
3. **Be accurate**: Ensure information is correct and up-to-date
4. **Be practical**: Offer actionable guidance and solutions
5. **Be organized**: Keep work structured and well-documented

## Working Environment
- This is a research and troubleshooting workspace
- Chat logs and findings are the primary artifacts
- Screenshots provide visual context
- your AI tool is the primary interface (works with any AI model: Claude, GPT, Gemini, etc.)
- Git is used for local version control and optional sync across devices via /push

## your AI tool Workflow
When working in this topic with your AI tool:

1. **Starting a chat**: Use `/chat start` to initialize a new research session
   - **AUTO-CLOSE**: Automatically closes any active chat before starting
   - Previous chat is committed with message "Research session: [title]"
2. **Screenshots**: Type "ss" or "/ss" to examine the latest screenshot
   - **STEP 1 - MANDATORY**: Run `/ss` (copies newest file to latest.png)
   - **STEP 2**: Read `/Users/levon/Development/levonbecker/template_ai_vault/screenshots/latest.png` (only AFTER step 1 - otherwise you get a stale image)
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

**Note**: `/chat start` and `/chat resume` now automatically close active chats - no need to manually run `/chat end` first.

## Available Commands
your AI tool slash commands (routed to Python modules):
- `/chat start` - Start a new chat session (auto-closes active chat)
- `/chat end` - Save complete chat log to file and deactivate session (does not commit/push)
- `/chat resume` - Resume a previous chat (auto-closes active chat)
- `/chat list` - List all chats in this topic
- `/repo pull` - Pull updates from git remote and iCloud
- `/repo push` - Push changes to git remote and iCloud
- `/repo view_screenshot` - Copy latest screenshot to latest.png (alias: `/ss`)

## Modifying Slash Commands - CRITICAL WORKFLOW
**IMPORTANT:** your AI tool caches command files. After making changes to `.opencode/command/*.md` files, you MUST restart your AI tool for changes to take effect.

**Workflow for modifying slash commands:**

1. **Make changes** to the command file (e.g., `.opencode/command/chat.md`)
2. **Save the file**
3. **DO NOT TEST YET** - changes won't work until restart
4. **Close your AI tool** completely (exit the application)
5. **Reopen/Restart your AI tool** in the same directory
6. **NOW test the command** - changes should be active

**Why this is necessary:**
- your AI tool loads and caches all command files at startup
- File changes are not hot-reloaded during runtime
- Testing before restart will show old cached behavior
- This applies to ALL command file changes (frontmatter, content, etc.)

**Common mistake:**
```
❌ WRONG: Edit file → Test immediately → Doesn't work → Get confused
✅ RIGHT: Edit file → Close your AI tool → Reopen → Test → Works!
```

## `/chat end` Workflow - CRITICAL AI AGENT INSTRUCTIONS
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
4. ❌ Does NOT push to remote (push manually when ready)

## File Organization
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

**Note**: Screenshots are stored centrally at repo root (`/Users/levon/Development/levonbecker/template_ai_vault/screenshots`), NOT in topic-specific folders.

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
- ✅ RIGHT: When requested, create `docs/domains.csv`, `docs/config.json`, or `docs/home_security/pricing.md`

## Screenshots Workflow
When user types `ss` or `/ss` to view a screenshot, follow these steps IN ORDER:

### Step 1 - Run the screenshot command
Use `/ss` (alias for `/repo view_screenshot`). It copies the most recent screenshot to `latest.png`.

### Step 2 - Read the copied file
```
/Users/levon/Development/levonbecker/template_ai_vault/screenshots/latest.png
```
Only read this AFTER step 1 completes successfully.

### Step 3 - Describe what you see
Describe the image content to help with the user's research.

**Common mistake to avoid:**
```
❌ WRONG: Read latest.png directly without running /ss first
✅ RIGHT: Run /ss → THEN read latest.png
```

## Best Practices
- Keep chats focused on specific topics or problems
- Use descriptive titles when starting chats
- Capture screenshots for visual context
- AI agents save complete chat logs with timestamps when `/chat end` is called
- Commit work frequently with meaningful messages
- Use `/chat end` at end of session to save locally, then `/push` when ready

## Collaboration
Work may be done using various AI models in your AI tool (Claude, GPT, Gemini, etc.). Maintain consistency and build on previous work when possible.
