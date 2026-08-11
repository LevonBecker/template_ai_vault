"""Template sync tasks — pull shared tooling from the parent template repo, or push it upstream.
Newly wired here (2026-08-11); the modules already existed but had no `invoke` task exposing them.
`context.run("python -m ...")`, matching every other task in this repo (see repo.py's docstring
for why — no `sys.path` insert in `tasks/__init__.py` here).
"""

from invoke import task


@task
def pull(context):
    """Resolve the local path to the parent template repo (clone from remote if not found locally)"""
    context.run("python -m modules.template.pull")


@task
def push_diff(context):
    """Diff this repo's scoped tooling against the parent template repo (ADDED/MODIFIED/DELETED)"""
    context.run("python -m modules.template.push diff")


@task
def push_apply(context, files="", deletes=""):
    """Copy approved files (and apply deletions) to a new branch in the parent template repo, then push it

    files/deletes are comma-separated relative paths, e.g. --files=modules/foo.py,tasks/foo.py
    """
    flags = ""
    for f in (f.strip() for f in files.split(",") if f.strip()):
        flags += f' --file="{f}"'
    for d in (d.strip() for d in deletes.split(",") if d.strip()):
        flags += f' --delete="{d}"'
    context.run(f"python -m modules.template.push apply{flags}")


@task
def push_create_pr(context, branch, title=None, body=None):
    """Open a PR for `branch` against the parent template repo (gh pr create)"""
    flags = f' --branch="{branch}"'
    if title:
        flags += f' --title="{title}"'
    if body:
        flags += f' --body="{body}"'
    context.run(f"python -m modules.template.push create-pr{flags}")
