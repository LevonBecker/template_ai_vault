from invoke import task

from . import claude, cline, hermes, opencode, ruff, tests


@task
def ai_sync(context, force=False):
    """Sync all AI tool commands from .github/prompts/ source of truth"""
    hermes.sync(context)
    claude.sync(context, force=force)
    cline.sync(context)
    opencode.sync(context, force=force)


@task
def fix(context):
    """Run All Automated Fixes"""
    ruff.fix(context)
    ruff.format(context)


@task
def test(context):
    """Run All Tests"""
    tests.actionlint(context)
    tests.pylint(context)
    tests.rufflint(context)
    tests.yamllint(context)
