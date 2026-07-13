---
name: quality
description: Use for template_ai_assistant quality workflows: run tests, fix lint failures, apply formatting, or use /test, /fix, or /claude equivalents.
---

# Quality Workflow

Use these `.github/prompts/` files as source of truth:

- `.github/prompts/test.prompt.md`
- `.github/prompts/fix.prompt.md`
- `.github/prompts/claude.prompt.md`

When the user asks to test, fix, or use an equivalent workflow, read the matching prompt file and follow it.

For Python or YAML changes, preserve the repository requirement to run:

```bash
uv run --no-sync invoke fix
uv run --no-sync invoke test
```

The required result is a 10/10 score with exit code 0 before committing.
