# Setup Module
One-time repo bootstrapping helpers, called by `setup.sh`.

## Commands
```sh
uv run --no-sync invoke setup.properties
```

## What It Does
`properties.yml` is gitignored **only in template repos** (this one and its siblings — anything
named `template_*`), since it would otherwise leak this machine's local paths into the template's
own history. In a real repo forked from a template (like ai_vault, this repo's own leaf
descendant), setup strips the ignore line from `.gitignore` the first time it runs there, so
`properties.yml` is committed like any other repo config — see `_sync_gitignore_tracking()`.
Creating the file itself is **a no-op if it already exists** — `modules/setup/properties.py` only
ever creates the file, it never rewrites an existing one (the gitignore check still runs every
time, though). To regenerate the file (e.g. after moving the repo, renaming it, or pointing it at a
new fork), delete or rename `properties.yml` first, then run again.

On first run, assembles it from every tier fragment under `modules/setup/templates/properties/*.yml`
— one file per repo in the lineage, each named after itself:
- `template_python.yml` — `repo`, `template` (the root; generic to every template-stamped repo
  regardless of product line)
- `template_ai_python.yml` — the AI-agent layer, generic to every AI-tooled repo
- `template_ai_vault.yml` — `icloud`, `screenshots` (generic to the ai_vault product line, tracked,
  synced via `/template`)

A descendant repo (e.g. `ai_vault`) adds its own same-named fragment on top for its own real
business config, without ever touching this repo's fragments.

`repos` (the GitHub org/repo map + template lineage) is built additively rather than concatenated:
each fragment's own `repos:` block contributes just its own org/repo + the lineage edge to its
parent, deep-merged into whatever was inherited from earlier tiers. A repo only ever ends up
knowing its own ancestor chain, never a sibling branch it isn't descended from.

Detects this repo's actual path on disk and its git `origin` remote (if any), and stamps
`repo.local`, `repo.remote`, and `screenshots.location` with those values. Auto-detects
`template.*` (the parent template repo for `/template`) via GitHub's generated-from link, falling
back to an interactive prompt.

## Files
- `properties.py` — creates `properties.yml` (used by `inv setup.properties`)
- `templates/properties/*.yml` — per-tier fragments merged into a fresh `properties.yml`
- `README.md` — this file
