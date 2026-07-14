# Custom Prompts (Slash Commands)
How the repo defines a slash command once and makes it work identically in every AI tool.

## Source of Truth
**`.github/prompts/*.prompt.md`** (GitHub Copilot's native prompt format) is the single source of
truth for every slash command. Four sync modules generate the tool-specific formats from it:

| Module | Generates | Invoke command |
|---|---|---|
| `modules/claude/sync.py` | `.claude/commands/*.md` | `inv claude.sync` |
| `modules/cline/sync.py` | `.clinerules/workflows/*.md` | `inv cline.sync` |
| `modules/hermes/sync.py` | `~/.hermes/config.yaml` + `SKILL.md` | `inv hermes.sync` |
| `modules/opencode/sync.py` | `.opencode/command/*.md` | `inv opencode.sync` |

Run everything at once:
```bash
uv run --no-sync invoke ai.sync
```

**Never hand-edit `.claude/commands/`, `.opencode/command/`, or `.clinerules/workflows/` directly**
— those are generated output. Edits there get silently overwritten (or diverge unnoticed) the next
time someone runs the corresponding sync with `--force`. Edit the `.github/prompts/*.prompt.md` file
and re-sync instead.

This is a different system from the AI *rules* hierarchy (`.github/instructions/`, delegated to via
`AGENTS.md`/`CLAUDE.md`) — see [`architecture.md`](architecture.md#two-separate-sync-systems) for how
the two relate.

## Required Frontmatter by Tool

### GitHub Copilot (`.github/prompts/*.prompt.md`) — write this one
```yaml
---
name: command_name
description: Brief description
argument-hint: arg1 | arg2 [optional]
agent: agent
---
```

### OpenCode (`.opencode/command/*.md`) — generated
```yaml
---
description: Brief description
agent: general
subtask: false  # CRITICAL — prevents Task tool recursion
slash_command: /command_name
---
```

### Claude Code (`.claude/commands/*.md`) — generated
```yaml
---
description: Brief description
---
```
Claude Code uses the filename as the command name; extra frontmatter fields are ignored.

## Command Body
All formats execute the same way — a thin wrapper that shells out to a router module:
```
!`uv run --no-sync python -m modules.your_module.route "$ARGUMENTS"`
```
The `!` prefix runs bash. `$ARGUMENTS` receives everything typed after the command name.

**All `uv run` calls in command files MUST include `--no-sync`** — it prevents an automatic
dependency sync on every single command invocation.

## Creating a New Command
1. **Python module** — `modules/your_module/your_task.py` (all business logic lives here)
2. **Router module** — `modules/your_module/route.py` (parses `$ARGUMENTS`, dispatches to the module)
   ```python
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
3. **Prompt file** — `.github/prompts/your_command.prompt.md` with the frontmatter + body above.
   This is the only command file you hand-write.
4. **Sync it out**: `uv run --no-sync invoke ai.sync` (generates the Claude/Cline/Hermes/OpenCode
   equivalents)
5. **Test**: `uv run --no-sync invoke fix && uv run --no-sync invoke test` — must be 10/10 for `.py`
   changes
6. Update the owning module's `README.md`

See `.github/instructions/commands.instructions.md` for the complete convention.

## Editing an Existing Command
1. Edit `.github/prompts/{name}.prompt.md`
2. Re-sync: `uv run --no-sync invoke ai.sync` (or the single-tool variant if you only need one)
3. **Restart your AI tool** — command files are cached at startup and are not hot-reloaded

```
❌ WRONG: Edit prompt file → sync → test immediately in the same session → stale cache, confused
✅ RIGHT: Edit prompt file → sync → restart AI tool → test → works
```

## `DO NOT`
- ❌ Put business logic in a command markdown file
- ❌ Write bash scripts directly inside a slash command body
- ❌ Use `subtask: true` in OpenCode frontmatter (causes Task tool recursion)
- ❌ Hand-edit generated files (`.claude/commands/`, `.opencode/command/`, `.clinerules/workflows/`)
- ❌ Omit `--no-sync` from `uv run` calls inside command files
