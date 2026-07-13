---
description: Check and update version configs (Python + libs)
agent: general
subtask: false
slash_command: /version
allowed-tools: Bash(uv run --no-sync *)
---

# version - Check and Update Version Configs

Check for Python and library updates, update configuration files.

## Usage

Check everything and update all configs:
!`uv run --no-sync python -m modules.versioning.route "$ARGUMENTS"`

Check and update only libraries:
!`uv run --no-sync python -m modules.versioning.route "libs"`

Check and update only Python:
!`uv run --no-sync python -m modules.versioning.route "python"`

Alias to /upgrade (backward compatibility):
!`uv run --no-sync python -m modules.versioning.route "upgrade"`

## Description

The version command checks for updates and modifies configuration files only.
It does NOT install anything - use /upgrade to actually install updates.

### What it does:
- Checks for latest Python stable version
- Checks for outdated library dependencies
- Updates config files (pyproject.toml, .python-version, etc.)
- Shows you what changed via git diff

### What it does NOT do:
- Does NOT install new Python versions
- Does NOT rebuild .venv
- Does NOT run uv sync

## Workflow

Best practice:
1. Run `/version` to check and update configs
2. Review changes with `git diff`
3. If satisfied, run `/upgrade` to install
4. If not, run `git restore .` to revert

## Examples

```bash
# Check everything
/version                    # Shows Python + libs, prompts to update configs

# Check specific components
/version libs               # Only check libraries
/version python             # Only check Python

# Auto-confirm (skip prompts)
/version --yes              # Update all configs without prompting

# Preview mode
/version --dry-run          # Show what would change, don't modify files
```

## Exit Codes

- 0: Config files updated
- 2: Cancelled by user
- 3: Already up to date
