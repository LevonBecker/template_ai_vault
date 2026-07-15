---
name: punch-it-chewy
description: Push the current feature branch, then draft PR notes and open a Pull Request via gh.
argument-hint: no arguments required
agent: agent
---

Run the push workflow:

!`uv run --no-sync python -m modules.repo.push`

Then follow the `/pr` steps: gather the branch/diff context via `uv run --no-sync invoke repo.pr_diff`,
write a `## Summary` and `## Changes` description, then create the PR with
`uv run --no-sync invoke repo.pr_create --title="<title>" --content="<notes>"`. Report the PR URL
to the user.
