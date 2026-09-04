# Setup — repo-local `properties.yml` fragments
The bootstrap code (`inv setup.properties`, called by `setup.sh`) is **shared** — it comes from
`fireball_sidecar_toolkit` and is clobbered into `modules/toolkit/setup/properties.py`. Never edit
it there.

What stays here is only the **per-tier YAML fragments** it reads — one file per repo in the
lineage, kept repo-local because they come from the parent repos, not the toolkit:
- `templates/properties/template_python.yml` — `repo`
- `templates/properties/template_ai_vault.yml` — `icloud`, `screenshots`
- `templates/properties/fireball_ai_vault.yml` — `fireball` (expense CSVs, COGS config)

## What the bootstrap does
`properties.yml` is gitignored **only in template repos** (`template_*`); this is a real repo, so
it is committed. On first run `modules/toolkit/setup/properties.py`:

1. Assembles `properties.yml` from every `templates/properties/*.yml` fragment, deep-merging each
   fragment's `repos:` block into one nested org/repo + lineage tree.
2. Detects this repo's path on disk and its git `origin` remote, stamping `repo.local`,
   `repo.remote`, and `screenshots.location`.
3. Prompts whether to enable iCloud sync if an `icloud` section is present.

A no-op if `properties.yml` already exists — to regenerate, delete it first. Shared AI tooling
comes from `invoke sidecar.toolkit.download`, not a `/template` sync (retired).
