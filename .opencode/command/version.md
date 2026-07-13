---
description: Check and update version configs (Python + libs)
subtask: false
agent: general
slash_command: /version
---

!`uv run --no-sync python -m modules.versioning.route "$ARGUMENTS"`
