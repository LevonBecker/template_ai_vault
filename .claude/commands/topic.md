---
description: Switch topics, list topics, or update topic configs
agent: general
subtask: false
slash_command: /topic
allowed-tools: Bash(uv run --no-sync *)
---

!`uv run --no-sync python -m modules.topic.route "$ARGUMENTS"`

If $ARGUMENTS starts with "list", render the command output as a tree showing all topics and subtopics. Mark the active topic with ⭐. End with a one-line summary (e.g. "42 topics — active: **bicycling**").

After running the command, if the output shows a topic switch (contains "Switched to:"):
- The **Full path** line in the output is now the active topic root for this conversation
- ALL subsequent relative paths resolve under that full path:
  - `docs/...` → `{topic_full_path}/docs/...`
  - `2026/...` → `{topic_full_path}/2026/...`
  - Any bare filename/folder → `{topic_full_path}/...`
- Do NOT use any previously cached topic path — the new path from this output is the source of truth
- Do NOT read `active_topic.yml` to determine the path; use the command output directly
