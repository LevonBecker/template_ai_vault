---
description: Push changes to git remote. Runs invoke fix, invoke test, then commits and pushes.
subtask: false
agent: general
slash_command: /push
---

!`uv run --no-sync python -m modules.repo.push`
