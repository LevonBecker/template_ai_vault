"""Route /version arguments to version modules."""

from __future__ import annotations

import shlex
import subprocess
import sys

from ..common.route_utils import build_env, find_repo_root


def _run(module: str, args: list[str]) -> int:
    repo_root = find_repo_root()
    env = build_env(repo_root)
    cmd = [sys.executable, "-m", module, *args]
    completed = subprocess.run(cmd, cwd=repo_root, env=env, check=False)
    return completed.returncode


def main() -> int:
    raw_args = sys.argv[1] if len(sys.argv) > 1 else ""
    args = shlex.split(raw_args)

    if not args:
        # No args: run combined check and update
        return _run("modules.versioning.check_all", [])

    first = args[0]
    rest = args[1:]

    if first == "libs":
        return _run("modules.versioning.libs", rest)

    if first == "python":
        return _run("modules.versioning.python", rest)

    if first == "upgrade":
        # Backward compatibility alias to /upgrade command
        return _run("modules.versioning.upgrade", rest)

    sys.stderr.write(f"Unknown version subcommand: {first}\n")
    sys.stderr.write("Usage: /version [libs | python | upgrade]\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
