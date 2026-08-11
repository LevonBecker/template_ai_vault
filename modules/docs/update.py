"""
Sync docs/change_logs/<category>/<name>.md entries from properties.yml.

Usage:
    uv run --no-sync python -m modules.docs.update
    uv run --no-sync invoke docs.update_changelogs
"""

import logging

from ..common import cli
from .lib import change_logs as lib_change_logs

LOGGER = logging.getLogger(__name__)


def change_logs() -> None:
    """Prepend any missing docs/change_logs/<category>/<name>.md entries from properties.yml."""
    LOGGER.info("Running Change Log Update")
    lib_change_logs.check_each_log(update=True)


@cli.command()
def main() -> None:
    """Entry point for `python -m modules.docs.update`."""
    change_logs()


if __name__ == "__main__":
    main()
