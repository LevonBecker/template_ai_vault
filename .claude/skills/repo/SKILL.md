---
name: repo
description: Use for generic /repo push|pull|cleanup|set_screenshots|view_screenshot requests — routes to the matching repo workflow. Equivalent to /repo.
---

# Repo Workflow

Use this file as source of truth: `.github/prompts/repo.prompt.md`

When the user asks for a repo subcommand not covered by a dedicated command (`push`, `pull`, `ss`),
read that prompt file and follow it.
