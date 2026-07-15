---
description: Run repository tests and style checks, auto-fix any errors
subtask: false
agent: general
slash_command: /test
---

Run repository tests and style checks, then auto-fix any errors found.

## Your Task

1. Call the invoke task to run tests:

```bash
uv run invoke test
```

2. If tests fail, analyze the output to determine what failed:
   - **Ruff linting errors**: Auto-fixable style issues
   - **Ruff format errors**: Auto-fixable formatting issues
   - **Mypy type errors**: May require manual fixes
   - **Other errors**: Analyze and fix as needed

3. For auto-fixable issues, run the fix task:

```bash
uv run --no-sync invoke fix
```

This runs both ruff check --fix and ruff format automatically.

4. For type errors or other issues:
   - Read the affected files
   - Analyze the errors
   - Fix the issues (prompt user if clarification needed)
   - Re-run tests to verify fixes

5. Repeat until all tests pass

## What the Test Command Does

The `uv run --no-sync invoke test` task (defined in `tasks/combos.py`) runs:
- **actionlint**: GitHub Actions workflow validation
- **pylint**: Python code quality checking
- **rufflint**: Python linting (style and best practices)
- **yamllint**: YAML file validation

## Auto-Fix Strategy

Most common issues can be auto-fixed with the fix task:

```bash
uv run --no-sync invoke fix
```

This automatically runs:
- `ruff check --fix .` - Fixes linting issues
- `ruff format .` - Fixes formatting issues

After auto-fixing, re-run tests to verify:

```bash
uv run --no-sync invoke test
```

## Manual Fix Strategy

For issues that can't be auto-fixed:

1. **Simple fixes** (unused imports, type errors, etc.):
   - Read the file with the error
   - Understand the error message
   - Apply the appropriate fix
   - Re-run tests
   - Iterate until clean

2. **Complex fixes** (code complexity, refactoring needed):
   - If the fix requires significant refactoring or user input
   - Present a **formatted list of remaining issues** to the user
   - Format: `File:Line - Rule: Description`
   - Let the user decide how to proceed

## Goal: 10/10 Code Quality

The user expects **10/10 code quality always**. This means:

- ✅ Auto-fix everything possible with `uv run --no-sync invoke fix`
- ✅ Manually fix simple issues (imports, types, etc.)
- ⚠️ **For complex issues that need refactoring or user input:**
  - Present a clean list of remaining offenses
  - Include: file path, line number, rule code, and description
  - Ask user how to proceed (refactor, exclude, adjust limits)
  - Don't commit until all issues are resolved or explicitly approved

## Presenting Remaining Issues

When issues require user input, format them like this:

```
## Remaining X Style Offenses

### 1. `modules/example/file.py:123` - `function_name()` (2 offenses)
- **RULE_CODE**: Description (actual > limit)
- **RULE_CODE**: Description (actual > limit)

### 2. `modules/another/file.py:456` - `other_function()` (1 offense)
- **RULE_CODE**: Description (actual > limit)
```

Then ask: "How would you like to proceed?"

## Important Notes

- Run from any directory in the repository
- Auto-fix when possible, manual fix when needed
- Always re-run tests after fixes to verify
- **For complex issues: present formatted list to user**
- Don't commit fixes automatically - let user review
- Target: **10/10 code quality score**

## Related Commands

- `/push` - Push changes after tests pass
- `/pull` - Pull latest before running tests
- `/chat end` - End active chat (save + commit)
