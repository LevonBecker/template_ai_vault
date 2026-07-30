---
description: Switch to the default branch, pull, and delete the merged local feature branch.
subtask: false
agent: general
slash_command: /pr-cleanup
---

!`uv run --no-sync python -m modules.repo.route "pr_cleanup"`
