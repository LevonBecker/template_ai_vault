# Setup Module
One-time and idempotent repo bootstrapping helpers, called by `setup.sh`.

## Commands
```sh
uv run --no-sync invoke setup.properties
```

## What It Does
`properties.yml` is committed in this repo — it also holds business-specific config (Fireball COGS
rates, financials paths) alongside the machine-specific paths below, so `modules/setup/properties.py`
only ever rewrites specific keys in place rather than treating the whole file as disposable:

1. If `properties.yml` doesn't exist, creates it from a built-in template (`_TEMPLATE` in the module).
2. Detects this repo's actual path on disk and its git `origin` remote (if any).
3. Rewrites only `repo.local`, `repo.remote`, and `screenshots.location` in place, targeting those
   specific keys by name — every comment, business-specific section, and the rest of the file's
   formatting survives untouched.

Safe to re-run any time: `uv run --no-sync invoke setup.properties`. Re-run it after moving the repo
on disk, renaming it, or pointing it at a new fork — it just re-stamps the same three fields with
freshly detected values.

`icloud.path` and `template.*` can't be auto-detected and are left alone once the file exists — edit
those by hand if you use those features.

## Why Not a Placeholder Token?
An earlier version used a literal token (e.g. `PATH_TO_REPO`) that got search-and-replaced. That only
works once — after the token is replaced with a real path, a second run has nothing left to find.
Targeting the YAML key by name works every time, regardless of what value is currently there, which is
what makes re-running after a move/rename safe.

## Files
- `properties.py` — creates/stamps `properties.yml` (used by `inv setup.properties`)
- `README.md` — this file
