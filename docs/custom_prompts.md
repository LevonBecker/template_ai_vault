# Custom Prompts (Slash Commands)
How the repo defines a slash command once and makes it work identically in every AI tool.

## Source of Truth
**`.github/prompts/*.prompt.md`** (GitHub Copilot's native prompt format) is the single source of
truth for every slash command. Two sync modules generate tool-specific formats from it; the
remaining two mirrors are hand-maintained copies of the same prompt body:

| Module | Generates | Invoke command |
|---|---|---|
| `modules/hermes/sync.py` | `~/.hermes/config.yaml` + `SKILL.md` | `inv hermes.sync` |
| `modules/opencode/sync.py` | `.opencode/command/*.md` | `inv opencode.sync` |

Run both at once:
```bash
uv run --no-sync invoke ai.sync
```

`.claude/commands/*.md` and `.clinerules/workflows/*.md` have no sync script — copy the prompt
body over by hand (converting exec syntax per tool, see below) whenever you add or edit a
`.github/prompts/*.prompt.md` file. `uv run --no-sync invoke tests.check_agents` verifies every
prompt has a matching file in both of these plus `.claude/skills/` and `.opencode/command/`, and
runs in CI. See `.github/instructions/prompts.instructions.md` for the full mirror conventions.

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

### Claude Code (`.claude/commands/*.md`) — hand-maintained mirror
```yaml
---
description: Brief description
---
```
Claude Code uses the filename as the command name; extra frontmatter fields are ignored.

### Cline (`.clinerules/workflows/*.md`) — hand-maintained mirror
No frontmatter — plain markdown body only, filename (minus extension) is the command name. Cline
has no inline `!`...`` exec syntax, so exec lines become "Run this terminal command:" followed by a
fenced code block instead.

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
4. **Sync it out**: `uv run --no-sync invoke ai.sync` (generates the Hermes/OpenCode equivalents)
5. **Mirror it by hand**: add `.claude/commands/your_command.md` and
   `.clinerules/workflows/your_command.md` (and `.claude/skills/your_command/SKILL.md` per
   `prompts.instructions.md`) — `uv run --no-sync invoke tests.check_agents` fails until all four
   exist
6. **Test**: `uv run --no-sync invoke fix && uv run --no-sync invoke test` — must be 10/10 for `.py`
   changes
7. Update the owning module's `README.md`

See `.github/instructions/commands.instructions.md` for the complete convention.

## Editing an Existing Command
1. Edit `.github/prompts/{name}.prompt.md`
2. Re-sync: `uv run --no-sync invoke ai.sync` (or the single-tool variant if you only need one)
3. Update `.claude/commands/{name}.md` and `.clinerules/workflows/{name}.md` by hand to match
4. **Restart your AI tool** — command files are cached at startup and are not hot-reloaded

```
❌ WRONG: Edit prompt file → sync → test immediately in the same session → stale cache, confused
✅ RIGHT: Edit prompt file → sync → restart AI tool → test → works
```

## `DO NOT`
- ❌ Put business logic in a command markdown file
- ❌ Write bash scripts directly inside a slash command body
- ❌ Use `subtask: true` in OpenCode frontmatter (causes Task tool recursion)
- ❌ Hand-edit generated files (`.opencode/command/`, Hermes's `~/.hermes/config.yaml` + `SKILL.md`)
- ❌ Let `.claude/commands/` or `.clinerules/workflows/` drift from `.github/prompts/` — run
  `uv run --no-sync invoke tests.check_agents` after touching any of the four dirs
- ❌ Omit `--no-sync` from `uv run` calls inside command files
