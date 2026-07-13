Run all tests:

Run this terminal command:

```
uv run --no-sync invoke test
```

If all tests pass, report success and stop.

If any tests fail:
- For Ruff offenses: attempt to auto-fix by running `uv run --no-sync invoke fix`, then re-run `uv run --no-sync invoke test` to confirm. If offenses remain after auto-fix, show the remaining failures and ask the user how they would like to proceed.
- For Pylint offenses (must score 10.00/10): show the offending lines and ask the user how they would like to proceed.
- For YAML lint failures: show the offending lines and ask the user how they would like to proceed.
- For actionlint failures: show the offending workflow file and line, and ask the user how they would like to proceed.
- For any other failures: show the full error output and ask the user how they would like to approach fixing it.
