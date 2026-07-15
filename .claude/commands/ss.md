---
description: View the latest screenshot from centralized screenshots folder
agent: general
subtask: false
slash_command: /ss
allowed-tools: Bash(uv run --no-sync *)
---

Run this terminal command to copy the latest screenshot to `latest.png`:

!`uv run --no-sync python -m modules.repo.route "view_screenshot"`

Then view the file at `screenshots/latest.png` (relative to the repository root).

Analyze the image and respond to $ARGUMENTS if provided, otherwise use the screenshot to continue helping with the current chat goal.
