---
description: Run Claude Code CLI directly with your Pro/Max subscription
subtask: false
agent: general
slash_command: /claude
allowed-tools: Bash(uv run --no-sync *)
---

Run `uv run --no-sync python -m modules.claude.route "$ARGUMENTS"` using the Bash tool.
