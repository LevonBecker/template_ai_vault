---
name: repo
description: Use for template_ai_assistant repository maintenance requests: repo pull, repo push, cleanup screenshots, set screenshots folder, view latest screenshot, /push, /pull, or /ss equivalents.
---

# Repo Workflow

Use these `.github/prompts/` files as source of truth:

- `.github/prompts/repo.prompt.md`
- `.github/prompts/push.prompt.md`
- `.github/prompts/pull.prompt.md`
- `.github/prompts/ss.prompt.md`

When the user asks for repository maintenance, read the matching prompt file and follow it. Translate natural language into the same arguments used by the prompt:

- Pull updates: `pull`
- Push changes: `push`
- Clean screenshots: `cleanup`
- Set screenshot location: `set_screenshots`
- View latest screenshot: `view_screenshot`

Run the repository router from the repo root:

```bash
uv run --no-sync python -m modules.repo.route "<arguments>"
```

For `/push`, `/pull`, and `/ss` equivalents, use the dedicated source prompt when present.
