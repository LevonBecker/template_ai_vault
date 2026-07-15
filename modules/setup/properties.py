"""
Stamp this machine's repo path (and git remote, if any) into properties.yml.

Idempotent and safe to re-run any time — e.g. after moving the repo on disk,
renaming it, or forking it to a new remote. Run via `inv setup.properties`
(called automatically by setup.sh, but you can re-run it directly whenever
the repo's location or remote changes).

properties.yml is committed in this repo (it also holds business-specific
config like Fireball COGS rates and financials paths), so unlike a fresh
fork's gitignored copy, this only ever rewrites specific keys in place. Only
repo.local, repo.remote, screenshots.location, and template.* are ever
touched, by targeting those specific keys (not a placeholder token — a token
would only be replaceable once, breaking re-runs after a move/rename). Every
other line, including comments and the business-specific sections, is left
exactly as-is.

template.* (this repo's parent template repo, used by /template) is
auto-detected from GitHub's generated-from link when possible, with an
interactive prompt as fallback — and is only ever written while it still
holds the built-in placeholder, so a hand-configured parent is never
clobbered.
"""

import re
import subprocess
from pathlib import Path

from modules.common import cli
from modules.common.utils import info, success

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_PROPERTIES_FILE = _REPO_ROOT / "properties.yml"

_TEMPLATE = """---
# AI Vault Repository Properties
# Central configuration for all scripts and automation.
#
# `inv setup.properties` (run automatically by setup.sh, and safe to re-run any time — e.g. after
# moving this repo, renaming it, or forking it to a new remote) creates this file from a built-in
# template on first run and re-stamps repo.local / repo.remote / screenshots.location on every
# run. template.* (the parent template repo for /template) is auto-detected from GitHub's
# generated-from link (or prompted for) while it still holds the placeholder — edit by hand any
# time. icloud.path is never auto-detected.

# Optional — off by default. Only needed if you sync this repo to an iCloud
# Obsidian vault for mobile access (see docs/). Set enabled: true and fill in
# path to turn on iCloud sync in /push and /pull.
icloud:
  enabled: false
  path: "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/<your-vault-name>/"

repo:
  local: "$HOME/path/to/this/repo"
  remote: "github.com/<your-username>/<your-repo-name>"

# This repo's parent template repo — where /template pulls shared tooling updates (modules/,
# tasks/, .github/, .claude/, etc.) from, and pushes generic improvements to as PRs. Repos chain
# (e.g. root skeleton -> domain template -> project repo); point this at the direct parent only.
# Optional — leave the placeholders if this repo doesn't sync with a template.
template:
  local: "$HOME/path/to/your/template/repo"
  remote: "github.com/<your-username>/<your-template-repo>"

screenshots:
  cleanup_patterns:
    - "*.png"
    - "*.jpg"
    - "*.jpeg"
    - "*.PNG"
    - "*.JPG"
    - "*.JPEG"
  latest_file: "latest.png"
  location: "$HOME/path/to/this/repo/screenshots"
  preserve_files:
    - "latest.png"
"""


_TEMPLATE_LOCAL_PLACEHOLDER = "$HOME/path/to/your/template/repo"
_TEMPLATE_REMOTE_PLACEHOLDER = "github.com/<your-username>/<your-template-repo>"


def _detect_repo_local() -> str:
    """Return this repo's absolute path, with $HOME swapped in for portability."""
    home = str(Path.home())
    repo_str = str(_REPO_ROOT)
    if repo_str.startswith(home):
        return "$HOME" + repo_str[len(home) :]
    return repo_str


def _detect_repo_remote() -> str | None:
    """Return the git origin remote as 'host/user/repo', or None if there isn't one."""
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=_REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None

    url = result.stdout.strip()
    url = re.sub(r"^git@([^:]+):", r"\1/", url)
    url = re.sub(r"^https?://", "", url)
    url = re.sub(r"\.git$", "", url)
    return url


def _detect_template_remote(repo_remote: str | None) -> str | None:
    """Return this repo's parent template as 'github.com/owner/name' via GitHub's generated-from link."""
    if not repo_remote or not repo_remote.startswith("github.com/"):
        return None
    try:
        result = subprocess.run(
            [
                "gh",
                "api",
                f"repos/{repo_remote.removeprefix('github.com/')}",
                "--jq",
                ".template_repository.full_name // empty",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None  # gh CLI not installed
    if result.returncode != 0:
        return None
    full_name = result.stdout.strip()
    return f"github.com/{full_name}" if full_name else None


def _read_scalar(lines: list[str], section: str, key: str) -> str | None:
    """Return the unquoted value of `key:` within a top-level `section:` block, or None."""
    in_section = False
    for line in lines:
        if line.rstrip("\n") == f"{section}:":
            in_section = True
            continue
        if not in_section:
            continue
        if line.strip() and not line[0].isspace():
            return None  # reached the next top-level key without finding it
        match = re.match(rf"^\s*{re.escape(key)}:\s*(.*?)\s*$", line)
        if match:
            return match.group(1).strip('"')
    return None


def _replace_scalar(lines: list[str], section: str, key: str, value: str, *, quote: bool = True) -> bool:
    """Rewrite `key: ...` to `key: value` within a top-level `section:` block, in place."""
    formatted = f'"{value}"' if quote else value
    in_section = False
    for i, line in enumerate(lines):
        if line.rstrip("\n") == f"{section}:":
            in_section = True
            continue
        if not in_section:
            continue
        if line.strip() and not line[0].isspace():
            return False  # reached the next top-level key without finding it
        match = re.match(rf"^(\s*{re.escape(key)}:\s*).*$", line)
        if match:
            lines[i] = f"{match.group(1)}{formatted}\n"
            return True
    return False


def _prompt_icloud_enabled(lines: list[str]) -> None:
    """Ask (interactively) whether to turn on iCloud sync for a freshly created properties.yml."""
    enabled = cli.confirm(
        "Enable iCloud sync for /push and /pull? (most people don't need this — off by default)",
        default=False,
    )
    _replace_scalar(lines, "icloud", "enabled", "true" if enabled else "false", quote=False)
    if enabled:
        info("iCloud sync enabled — edit icloud.path in properties.yml to your Obsidian vault path")


def _stamp_template_parent(lines: list[str], repo_local: str, repo_remote: str | None) -> None:
    """Fill in template.* (the /template parent) while it still holds the placeholder.

    Auto-detects via GitHub's generated-from link, falling back to an interactive prompt.
    A hand-configured (non-placeholder) parent is never touched.
    """
    current = _read_scalar(lines, "template", "remote")
    if current not in (None, "", _TEMPLATE_REMOTE_PLACEHOLDER):
        return

    remote = _detect_template_remote(repo_remote)
    if remote:
        info(f"Detected parent template repo (GitHub generated-from): {remote}")
    elif cli.confirm("Sync shared tooling with a parent template repo via /template?", default=False):
        remote = cli.prompt("Parent template remote (e.g. github.com/<user>/<template-repo>)")

    if not remote:
        info("No parent template repo configured — edit template.* in properties.yml if you add one later")
        return

    template_local = f"{repo_local.rsplit('/', 1)[0]}/{remote.rstrip('/').rsplit('/', 1)[-1]}"
    _replace_scalar(lines, "template", "remote", remote)
    _replace_scalar(lines, "template", "local", template_local)
    success(f"properties.yml: template.remote = {remote}")
    success(f"properties.yml: template.local = {template_local} (sibling-path guess — edit if it lives elsewhere)")


@cli.command()
def main() -> None:
    """Create properties.yml from the built-in template (if missing) and stamp local paths into it."""
    just_created = not _PROPERTIES_FILE.exists()
    if just_created:
        _PROPERTIES_FILE.write_text(_TEMPLATE)
        info("Created properties.yml")

    repo_local = _detect_repo_local()
    repo_remote = _detect_repo_remote()

    lines = _PROPERTIES_FILE.read_text().splitlines(keepends=True)
    _replace_scalar(lines, "repo", "local", repo_local)
    if repo_remote:
        _replace_scalar(lines, "repo", "remote", repo_remote)
    _replace_scalar(lines, "screenshots", "location", f"{repo_local}/screenshots")
    _stamp_template_parent(lines, repo_local, repo_remote)
    if just_created:
        _prompt_icloud_enabled(lines)
    _PROPERTIES_FILE.write_text("".join(lines))

    success(f"properties.yml: repo.local = {repo_local}")
    if repo_remote:
        success(f"properties.yml: repo.remote = {repo_remote}")
    else:
        info("No git remote 'origin' found — repo.remote left unchanged")
    success(f"properties.yml: screenshots.location = {repo_local}/screenshots")


if __name__ == "__main__":
    main()
