"""Route /sync-setup to the skeleton sync module."""

from __future__ import annotations

import shlex
import subprocess
import sys

from ..common.route_utils import build_env, find_repo_root


def main() -> int:
    raw_args = sys.argv[1] if len(sys.argv) > 1 else ""
    args = shlex.split(raw_args)

    repo_root = find_repo_root()
    env = build_env(repo_root)
    cmd = [sys.executable, "-m", "modules.skeleton.sync", *args]
    completed = subprocess.run(cmd, cwd=repo_root, env=env, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
