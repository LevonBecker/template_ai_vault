from invoke import task

from .. import hermes, opencode
from ..tests import actionlint, check_agents, pylint, rufflint, yamllint
from . import ruff


@task
def ai_sync(context, force=False):
    """Sync all AI tool commands from .github/prompts/ source of truth"""
    hermes.sync(context)
    opencode.sync(context, force=force)


@task
def fix(context):
    """Run All Automated Fixes"""
    ruff.fix(context)
    ruff.format(context)


@task
def test(context):
    """Run All Tests"""
    actionlint(context)
    check_agents(context)
    pylint(context)
    rufflint(context)
    yamllint(context)
