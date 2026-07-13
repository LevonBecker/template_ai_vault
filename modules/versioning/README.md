# Versioning Module
Checks project version configs against the latest published releases and updates the locks —
it does not install anything or run any workflow. Installing is a separate, explicit step
(`/upgrade` / `invoke upgrade.*`).

## Usage
```sh
uv run --no-sync invoke versioning.libs                  # check pyproject.toml deps, prompt to update
uv run --no-sync invoke versioning.workflows             # check .github/workflows/ action refs, prompt to update
uv run --no-sync invoke versioning.all                   # run every version check (libs, workflows)
uv run --no-sync invoke versioning.libs --dry-run        # preview only, never writes
uv run --no-sync invoke versioning.libs --yes            # skip the confirmation prompt

uv run --no-sync python -m modules.versioning.route "$ARGUMENTS"   # /version command router
```

## Files
- `route.py` — routes `/version` arguments: no args → `check_all`, or `libs` / `python` / `upgrade`
- `check_all.py` — combined check: Python version + pyproject.toml dependencies, one confirmation
- `libs.py` — checks `[project.dependencies]` and `[project.optional-dependencies]` against
  latest releases via `uv pip list --outdated`, rewrites version locks in `pyproject.toml`
  preserving constraint operators (exits `3` when everything is already up to date)
- `python.py` — checks the pinned Python version against the latest release and updates config
  file references
- `workflows.py` — scans `.github/workflows/*.yml` for `uses: owner/repo@vN` refs, compares against
  the highest published major tag (`git ls-remote`, no API token), and rewrites the pins in place;
  SHAs, branch refs, and full semver pins are left alone
- `upgrade.py` / `uv_sync.py` — install/sync helpers used by `/upgrade`

`libs.py` and `workflows.py` only edit config files — review the diff before committing.
