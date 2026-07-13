"""Route /claude arguments to Claude CLI."""

from __future__ import annotations

import subprocess
import sys

from ..common.route_utils import build_env, find_repo_root


def main() -> int:
    repo_root = find_repo_root()
    env = build_env(repo_root)
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    cmd = ["claude", *args]
    return subprocess.run(cmd, cwd=repo_root, env=env, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
