---
name: "update"
description: "Check pyproject.toml dependencies, the pinned Python version, and .github/workflows/ action refs against their latest published releases and update version locks. Does not install or run anything."
argument-hint: "[libs | python | workflows | update]"
agent: "sidecar-agent"
---
Use this file as source of truth: .github/prompts/update.prompt.md
