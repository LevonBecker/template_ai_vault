---
description: Manage chats (start, end, list, resume)
subtask: false
agent: general
slash_command: /chat
---

**CRITICAL for `end` subcommand — read this BEFORE running anything:**

If $ARGUMENTS is "end":
1. Read the active chat file (check `active.yml` in the active topic dir for the filename)
2. Replace the `## Overview` placeholder with a compact summary of this session
3. Append all conversation turns under `## Chat Log` using this EXACT format:
   ```
   **[YYYY-MM-DD HH:MM] User:** <message summary>

   **[YYYY-MM-DD HH:MM] Assistant:** <response summary>
   ```
   Use today's date and approximate times. The brackets, date, time, and role label are all required.
4. Only AFTER the file is written, run the command via Bash tool:
   `uv run --no-sync python -m modules.chat.route "end"`
Do NOT run the command first. Write the file first, then run once.

---

For all other subcommands (start, list, resume), run immediately:

`uv run --no-sync python -m modules.chat.route "$ARGUMENTS"`

If $ARGUMENTS starts with "list", render the command output as a markdown table with columns: # | Date | Title. Place the active chat (marked ⭐ active) as the last row, separated by a divider. Do not add extra commentary — just the table followed by a one-line summary (e.g. "24 chats — active: **a body on curve**").
