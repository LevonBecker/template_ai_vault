"""Create a new topic directory and initialize it with AI instruction files."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from ..common import cli as click
from ..common.properties import get_repo_local
from ..common.utils import error, info


@click.command()
@click.option("--path", required=True, help="Topic path relative to topics/ (e.g., 'health/dental')")
@click.option("--description", "-d", default=None, help="Optional description for the topic")
def main(path: str, description: str | None = None) -> None:
    """
    Create a new topic directory at the given path and run topic init in it.

    Always creates at topics/<path>. Use /topic <path> to switch to existing topics.
    """
    repo_local = get_repo_local()
    topics_root = repo_local / "topics"
    topic_dir = topics_root / Path(path)

    if topic_dir.exists():
        error(f"Topic already exists: topics/{path}\n💡 Use /topic {path} to switch to it.")

    # Create the directory
    topic_dir.mkdir(parents=True, exist_ok=True)
    info(f"Created topic directory: topics/{path}")

    # Run init from repo root, pointing AI_ASSISTANT_ORIGINAL_CWD at new topic dir
    cmd = [sys.executable, "-m", "modules.topic.init"]
    if description:
        cmd.append(f"--description={description}")
    env = os.environ.copy()
    env["AI_ASSISTANT_ORIGINAL_CWD"] = str(topic_dir)
    subprocess.run(cmd, cwd=repo_local, env=env, check=False)

    click.echo(f"✅ New topic ready: topics/{path}")
    click.echo(f"💡 Use /topic {path} to switch to it.")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
