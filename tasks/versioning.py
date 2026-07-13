"""Version-lock check tasks — compare pyproject.toml deps and workflow actions against latest releases."""

from invoke import task

# libs exits 3 when everything is already up to date
_OK_EXIT_CODES = (0, 3)


def _run_module(context, module, dry_run, yes):
    flags = ""
    if dry_run:
        flags += " --dry-run"
    if yes:
        flags += " --yes"
    result = context.run(f"python -m {module}{flags}", warn=True)
    if result.exited not in _OK_EXIT_CODES:
        raise SystemExit(result.exited)


@task
def libs(context, dry_run=False, yes=False):
    """Check pyproject.toml dependencies against latest releases and update version locks"""
    _run_module(context, "modules.versioning.libs", dry_run, yes)


@task
def workflows(context, dry_run=False, yes=False):
    """Check .github/workflows/ action refs against latest major versions and update them"""
    _run_module(context, "modules.versioning.workflows", dry_run, yes)


@task
def all(context, dry_run=False, yes=False):  # noqa: A001  # pylint: disable=redefined-builtin
    """Run every version check (libs, workflows)"""
    libs(context, dry_run=dry_run, yes=yes)
    workflows(context, dry_run=dry_run, yes=yes)
