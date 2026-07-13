---
description: View the latest screenshot from centralized screenshots folder
subtask: false
agent: general
slash_command: /ss
---

!`uv run --no-sync python -m modules.repo.route "view_screenshot"`

Then use the `view_image` tool on `$HOME/Development/levonbecker/template_ai_vault/screenshots/latest.png` to view the screenshot.

Analyze the image and respond to $ARGUMENTS if provided, otherwise use the screenshot to continue helping with the current chat goal.
