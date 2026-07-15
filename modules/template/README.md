# Template Module

Syncs shared, generic tooling between this repo and `template_ai_vault` via `/sync_template`.

## The chain

```
template_python  →  template_ai_vault  →  template_ai_vault
```

`template_python` is the root Python project skeleton. `template_ai_vault` is a derivative of it
that adds template_ai_vault-specific generic conventions (modules, `.agents/skills/`, hub instructions,
prompts, etc.) and is responsible for absorbing `template_python`'s own updates on its own — that
happens inside `template_ai_vault`, not here. This repo (`template_ai_vault`) only ever talks to
`template_ai_vault`.

## Usage

```sh
uv run --no-sync python -m modules.template.route              # pull (default)
uv run --no-sync python -m modules.template.route "push diff"  # push, phase 1
```

## Pull

Resolves `template.local` from `properties.yml`. If that path exists on disk, it's used directly —
no `git pull` is run, since the assumption is you already pushed your changes there before running
`/sync_template` here. If the local path isn't found (e.g. a different machine or CI), it
shallow-clones `template.remote` into `tmp/template_sync/` instead.

Either way, the resolved path is printed on its own line as `TEMPLATE_PATH=<path>` so the
`/sync_template` prompt can parse it out of any other output.

The actual file-by-file comparison, classification (shared tooling vs. project-specific), and
conflict resolution happens in the `/sync_template` prompt itself, not here — see
`.github/prompts/sync_template.prompt.md`.

## Push

Proposes new generic template_ai_vault improvements (in `modules/`, `.github/instructions/`,
`.github/prompts/`, `.claude/commands/`, `.clinerules/workflows/`, `.opencode/command/`,
`.agents/skills/` — excluding business-specific fireball/product-metadata content, see
`modules/template/scope.py`) into `template_ai_vault` as a pull request.

Three phases, split at the confirmation boundary so the agent can check in with the user between
each step:

1. `push diff` — enumerates and diffs the scoped candidates against `template_ai_vault`, printing
   `ADDED:`/`MODIFIED:` lists.
2. `push apply --file <path> ...` — for the files the user approved: fetches/updates
   `template_ai_vault`'s default branch, creates a new `sync-from-ai-vault-<timestamp>` branch,
   copies the files in, commits, and pushes the branch. Does **not** open a PR.
3. `push create-pr --branch <name> [--title ...] [--body ...]` — opens the PR via `gh pr create`.
   Confirms with the user first in interactive runs.

## Architecture

```
uv run --no-sync python -m modules.template.route ["pull" | "push <mode> ..."]
  ↓
modules/template/route.py
  ↓                                    ↓
modules/template/pull.py         modules/template/push.py
  ↓                                    ↓
modules/template/resolve.py  ←────┘  (shared local-path-or-clone resolution)
                                       modules/template/scope.py (fixed include/exclude rules)
  ↓
properties.yml (template.local / template.remote)  →  TEMPLATE_PATH=<resolved path>
```
