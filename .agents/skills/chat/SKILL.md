---
name: chat
description: Use for template_ai_assistant chat lifecycle requests: start chat, end chat, list chats, resume chat, close active chat, save chat logs, or manage topic chat files.
---

# Chat Workflow

Use `.github/prompts/chat.prompt.md` as the source of truth.

When the user asks for a chat lifecycle action, read that prompt file and follow it. Translate natural language into the same arguments used by the Copilot prompt:

- Start a chat: `start <title>`
- End or close the active chat: `end`
- List chats: `list [sort]`
- Resume a chat: `resume [pattern]`

Run the repository router from the repo root:

```bash
uv run --no-sync python -m modules.chat.route "<arguments>"
```

Preserve the prompt's output rules, especially the table rendering rule for chat lists and the `/chat end` failure behavior.
