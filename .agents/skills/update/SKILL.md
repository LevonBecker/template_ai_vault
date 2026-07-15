---
name: update
description: Use for template_ai_vault version and upgrade requests: check Python, library, or workflow-action versions, update configs, run upgrades, sync dependencies, /update, or /upgrade equivalents.
---

# Update Workflow

Use these `.github/prompts/` files as source of truth:

- `.github/prompts/update.prompt.md`
- `.github/prompts/upgrade.prompt.md`

When the user asks for version checks or upgrades, read the matching prompt file and follow it. Preserve the repository workflow (mirrors `apt update && apt upgrade`):

1. Run `/update`-equivalent checks before upgrades unless the user explicitly asks to upgrade.
2. Use `uv run --no-sync` for command execution.
3. Review diffs before upgrade actions when the source prompt requires it.

Run the appropriate repository router/module command from the repo root exactly as the source prompt specifies.
