---
name: template
description: Use for syncing shared generic tooling between template_ai_vault and the template_ai_vault repo — pulling template updates in, or pushing new generic template_ai_vault improvements out as a PR. Equivalent to /sync_template.
---

# Template Sync Workflow

Use this file as source of truth: `.github/prompts/sync_template.prompt.md`

When the user asks to sync tooling from the template repo, or to propose new generic
improvements upstream to `template_ai_vault`, read that prompt file and follow it.

- Pull template updates in (default): `pull` (or no argument)
- Push new generic tooling out as a PR: `push`

Run the router from the repo root:

```bash
uv run --no-sync python -m modules.template.route "<arguments>"
```

This is distinct from `/push` and `/pull` (see the `repo` skill), which push/pull the template_ai_vault
repo itself to/from its own GitHub origin and iCloud — `/sync_template` instead exchanges shared
generic tooling with the separate `template_ai_vault` repository.
