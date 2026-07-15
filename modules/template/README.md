# Template Module

Syncs shared, generic tooling between this repo and its **parent template repo** via
`/template`. The parent is configured in `properties.yml` (stamped automatically by
`inv setup.properties` when GitHub's generated-from link is available):

```yaml
template:
  local: "$HOME/path/to/parent-template-repo"
  remote: "github.com/<user>/<parent-template-repo>"
```

## The chain

```
root skeleton  →  domain template  →  project repo
```

Repos form a chain, and each repo syncs **only with its direct parent**. A domain template absorbs
the root skeleton's updates by running `/template` inside itself (its own `properties.yml`
points at the root skeleton) — never from further down the chain. To move a change across the whole
chain, sync it one hop at a time: push it up to the parent, then run `/template push` inside
the parent to continue upward (or pull downward hop by hop).

## Usage

```sh
uv run --no-sync python -m modules.template.route              # pull (default)
uv run --no-sync python -m modules.template.route "push diff"  # push, phase 1
```

## Pull

Resolves `template.local` from `properties.yml`. If that path exists on disk, it's used directly —
no `git pull` is run, since the assumption is you already pushed your changes there before running
`/template` here. If the local path isn't found (e.g. a different machine or CI), it
shallow-clones `template.remote` into `tmp/template_sync/` instead.

Either way, the resolved path is printed on its own line as `TEMPLATE_PATH=<path>` so the
`/template` prompt can parse it out of any other output.

The actual file-by-file comparison, classification (shared tooling vs. project-specific), and
conflict resolution happens in the `/template` prompt itself, not here — see
`.github/prompts/template.prompt.md`.

## Push

Proposes new generic improvements from this repo (in `modules/`, `.github/instructions/`,
`.github/prompts/`, `.claude/commands/`, `.clinerules/workflows/`, `.opencode/command/`,
`.agents/skills/` — excluding business-specific fireball/product-metadata content, see
`modules/template/scope.py`) into the parent template repo as a pull request.

Three phases, split at the confirmation boundary so the agent can check in with the user between
each step:

1. `push diff` — enumerates and diffs the scoped candidates against the parent template repo,
   printing `ADDED:`/`MODIFIED:`/`DELETED:` lists.
2. `push apply --file <path> ... [--delete <path> ...]` — for the changes the user approved:
   fetches/updates the parent's default branch, creates a new `sync-from-<repo>-<timestamp>`
   branch, copies the files in (and applies approved deletions), commits, and pushes the branch.
   Does **not** open a PR.
3. `push create-pr --branch <name> [--title ...] [--body ...]` — opens the PR via `gh pr create`.
   Confirms with the user first in interactive runs.

Repo-name references are rewritten on copy (this repo's name → the parent's name, both derived
from `properties.yml` `repo.local`/`template.local` basenames), so name-only differences never
need hand-editing.

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
