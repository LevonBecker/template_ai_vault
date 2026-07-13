---
applyTo: "**"
---
# Architecture Instructions

## Core Principle

**Commands are thin wrappers. Logic lives in Python modules.**

## Three-Layer Pattern

```
User → AI Tool Slash Command → Router Module → Python Module
```

- **Layer 1 (Commands)**: `.opencode/command/`, `.claude/commands/`, `.github/prompts/` — thin wrappers only, no logic
- **Layer 2 (Routers)**: `modules/*/route.py` — parse `$ARGUMENTS`, dispatch to module
- **Layer 3 (Modules)**: `modules/*/` — ALL business logic, reusable, testable

## Active State Files

| File | Location | Purpose |
|------|----------|---------|
| `active.yml` | `topics/<path>/` | Tracks active chat in a topic |
| `active_topic.yml` | repo root | Tracks currently active topic |

Both are git-ignored.

## Repository Boundaries

- **NEVER** write files outside `$HOME/Development/levonbecker/template_ai_vault`
- Repo root is defined in `properties.yml` under `repo.local`
- Use `modules/repo/fetch_properties.py` for all path resolution

## Multi-Tool Command Directory Layout

```
.opencode/command/    # OpenCode slash commands
.claude/commands/     # Claude Code slash commands
.github/prompts/      # GitHub Copilot prompt files
```

All three dirs contain equivalent commands — keep them in sync when adding new commands.

## AI Provider Architecture

### Source of Truth

**`.github/instructions/` is the one and only source of truth for all AI rules.**

All providers ultimately read from here. Never duplicate rules into provider-specific files — update the instruction files and let providers pick them up.

### Provider Hierarchy

| Priority | Provider | Config files read | How rules flow in |
|----------|----------|-------------------|-------------------|
| 1 (primary) | **GitHub Copilot** | `.github/instructions/*.md` | Native — `applyTo` frontmatter auto-applies files to matching paths |
| 2 | **OpenCode** | `AGENTS.md` (repo root) | `AGENTS.md` is a thin pointer; all substance is in `.github/instructions/` |
| 3 | **Claude TUI** | `CLAUDE.md` → `AGENTS.md` | `CLAUDE.md` delegates to `AGENTS.md`, which delegates to `.github/instructions/` |

### File Roles

| File | Role | Contents |
|------|------|----------|
| `.github/instructions/*.md` | **Source of truth** — update here only | All rules, standards, workflow |
| `AGENTS.md` (root) | Thin pointer for OpenCode / other tools | Slash command quick-ref + links to instruction files |
| `CLAUDE.md` (root) | Thin pointer for Claude TUI | One-liner pointing to `AGENTS.md` |
| `topics/*/AGENTS.md` | Topic-scoped pointer | Topic context + link to root `AGENTS.md` |
| `topics/*/CLAUDE.md` | Topic-scoped pointer for Claude | Points to topic `AGENTS.md` |

### Adding a New Provider

1. Check whether it natively reads `.github/instructions/` — if yes, nothing extra needed.
2. If not, create a thin entrypoint file (e.g. `NEWPROVIDER.md`) that reads:
   > "See `AGENTS.md` for all instructions. `.github/instructions/` is the source of truth."
3. Do **not** copy rules into the new file — always delegate.

### Removing a Provider

Delete its entrypoint file(s) only. `.github/instructions/` and `AGENTS.md` stay untouched.

- Remove OpenCode → delete `.opencode/` dir + `AGENTS.md` (if no other tool needs it)
- Remove Claude → delete `CLAUDE.md` + `.claude/` dir

## Documentation

- `.github/instructions/arch.instructions.md` — architecture standards and layering (this file)
- `.github/instructions/commands.instructions.md` — slash command standards and templates
- `.github/instructions/modules.instructions.md` — Python module architecture rules
- `.github/instructions/tests.instructions.md` — testing requirements and workflow
- `.github/instructions/project.instructions.md` — repository-wide operating rules
- `.github/instructions/topics.instructions.md` — topic and research document workflow
