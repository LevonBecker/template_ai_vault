---
description: Anchored squash of all commits to the root commit. Prompts to review the message, confirm squash, and optionally force push.
subtask: false
agent: general
slash_command: /squash
---

!`uv run --no-sync python -m modules.repo.route "squash"`

If it fails or reports a conflict, show the full output to the user and ask how they'd like to
proceed — do not force-push or retry automatically.
