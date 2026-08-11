# Docs Module
Changelog sync — keeps `docs/change_logs/<category>/<name>.md` in sync with `properties.yml`.

## Commands
```sh
uv run --no-sync invoke docs.update_changelogs
```

## What It Does
Each root `properties.yml` key listed in `lib/change_logs.py`'s `CHANGELOG_CATEGORIES` tuple owns
a change log per entry under `docs/change_logs/<category>/<name>.md`. `CHANGELOG_CATEGORIES` is
empty in this repo — nothing here is version-tracked yet, so both the sync task and its
drift-test counterpart (`tests/drift/docs/test_changelogs_current.py`) are no-ops until a
category is added. See `.github/instructions/docs.instructions.md` for the full `properties.yml`
entry shape and rendered markdown format.

## Files
- `update.py` — `change_logs()` + the `python -m modules.docs.update` CLI entry point, called by
  `tasks/ai/docs.py`
- `lib/change_logs.py` — the actual sync logic (`check_each_log`, used both by
  `invoke docs.update_changelogs` with `update=True` and the drift test with `update=False`)
- `README.md` — this file
