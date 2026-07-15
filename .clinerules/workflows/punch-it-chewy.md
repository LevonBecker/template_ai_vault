Run the push workflow:

Run this terminal command:

```
uv run --no-sync python -m modules.repo.push
```

Then follow the `/pr` steps: gather the branch/diff context via `uv run --no-sync invoke repo.pr_diff`,
write a `## Summary` and `## Changes` description, then create the PR with
`uv run --no-sync invoke repo.pr_create --title="<title>" --content="<notes>"`. Report the PR URL
to the user.
