---
name: topic
description: Use for template_ai_assistant topic requests: list topics, switch topic, initialize topic, update topic instructions, active topic, or topic navigation.
---

# Topic Workflow

Use `.github/prompts/topic.prompt.md` as the source of truth.

When the user asks for a topic action, read that prompt file and follow it. Translate natural language into the same arguments used by the Copilot prompt:

- List topics: `list`
- Switch topic: `switch <path>` or `<path>`
- Initialize topic: `init [description]`
- Update topic instructions: `update [--dry-run] [--current-only]`

Run the repository router from the repo root:

```bash
uv run --no-sync python -m modules.topic.route "<arguments>"
```

Keep topic file behavior aligned with repository instructions: topic guidance belongs in `AGENTS.md`, with `CLAUDE.md` as a thin pointer.
