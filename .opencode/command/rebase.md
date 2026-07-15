---
description: Rebase current branch onto the remote default branch. Optionally runs squash first before rebasing.
subtask: false
agent: general
slash_command: /rebase
---

!`uv run --no-sync python -m modules.repo.route "rebase"`

If it fails (e.g. merge conflicts during the rebase), show the full output to the user and ask how
they'd like to proceed — do not run further git commands automatically.
