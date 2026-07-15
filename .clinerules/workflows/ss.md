Run this terminal command:

```
uv run --no-sync python -m modules.repo.route "view_screenshot"
```

Then use the `view_image` tool on `screenshots/latest.png` (relative to the repository root) to view the screenshot.

Analyze the image and respond to $ARGUMENTS if provided, otherwise use the screenshot to continue helping with the current chat goal.
