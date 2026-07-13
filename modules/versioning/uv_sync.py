"""Sync and upgrade project dependencies via uv."""

from __future__ import annotations

import subprocess

from ..common.utils import error, info, success


def main() -> None:
    info("Syncing dependencies with uv...")

    result = subprocess.run(
        ["uv", "sync", "--upgrade"],
        check=False,
    )

    if result.returncode != 0:
        error("uv sync --upgrade failed")

    success("Dependencies synced")


if __name__ == "__main__":
    main()
