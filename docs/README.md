# Documentation
The top-level [`README.md`](../README.md) covers the basics (topics, chats, screenshots, repo sync).
This directory covers everything else, split by topic:

| File | Covers |
|---|---|
| [`setup.md`](setup.md) | Full install: `./setup.sh`, AI service auth, optional CLI tools, verifying the install |
| [`architecture.md`](architecture.md) | Repository structure, the rules vs. commands sync systems, module layout, coding conventions |
| [`commands.md`](commands.md) | Complete slash command reference (chat, topic, repo, PR workflow, versioning, etc.) |
| [`screenshots.md`](screenshots.md) | How `/ss` works, and the macOS commands to default screenshots into `screenshots/` |
| [`custom_prompts.md`](custom_prompts.md) | How `.github/prompts/` is the source of truth for commands, and how to add/edit one |

AI-agent-facing **rules** (what Claude Code / Copilot / OpenCode should do, file placement
conventions, etc.) live in `.github/instructions/` — start at
`.github/instructions/project.instructions.md` if you're customizing agent behavior rather than
using the repo. Those files are the source of truth for behavior; the pages above are the source of
truth for how a human sets up and drives the repo. See
[`architecture.md`](architecture.md#two-separate-sync-systems) for how the two relate.
