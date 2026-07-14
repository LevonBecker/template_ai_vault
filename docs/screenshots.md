# Screenshots
- Centralized location: `screenshots/` at repo root (shared by all topics — never a per-topic
  `screenshots/` subfolder)
- macOS: `Cmd+Shift+3`/`4` saves there automatically once configured (`/repo set_screenshots`)
- Type `/ss` (or `/repo view_screenshot`) to have the AI view the latest screenshot
- `latest.png` is a scratch working file — always the most recently copied screenshot
- Reference screenshots by repo-relative path (`screenshots/latest.png`), never an absolute path
- Git LFS tracks `*.png`, `*.jpg`, `*.svg`

Agent-facing rules for this folder live in `.github/instructions/screenshots.instructions.md`. This
page is the how-to/setup guide.

## How `/ss` Works
`/ss` is a shortcut for handing the AI whatever is currently on your screen — no need to save a file
somewhere and describe the path. It's especially useful for software/app troubleshooting: hit a weird
error, get stuck in a UI, or want a second opinion on something visual, and instead of typing out a
description you just screenshot it and say `/ss`.

**Workflow:**
1. Take a screenshot as normal:
   - `Cmd+Shift+3` — full screen
   - `Cmd+Shift+4` — region (drag to select an area)
   - `Cmd+Shift+4`, then `Space` — window (cursor turns into a camera; click a window to capture just it)

   Once `/repo set_screenshots` has been run, these save straight to the repo's `screenshots/` folder
   instead of the Desktop.
2. In chat, type `/ss` (optionally with a question, e.g. `/ss what's causing this error?`).
3. This copies the most recent screenshot to `screenshots/latest.png` and has the AI read it as an
   image, using it as context for the rest of the conversation.

Because `latest.png` is just a working/scratch file, you can `/ss` again after taking a new screenshot
and the AI will pick up the newest one — handy for multi-step visual debugging ("try that, then `/ss`
again to show me the result").

## Setting macOS to Default to `screenshots/`
`/repo set_screenshots` automates this, but here's what it's doing under the hood if you want to set it
manually or verify it. Replace `$HOME/path/to/repo/screenshots` with your actual repo's `screenshots/`
folder (e.g. `$HOME/Development/levonbecker/template_ai_vault/screenshots`):

```bash
# Point macOS screenshot captures at the repo's screenshots/ folder
defaults write com.apple.screencapture location "$HOME/path/to/repo/screenshots"

# Optional: skip the floating thumbnail preview so captures save immediately
defaults write com.apple.screencapture show-thumbnail -bool false

# Restart the UI service so the new location takes effect
killall SystemUIServer
```

To revert to the default Desktop location:
```bash
defaults delete com.apple.screencapture location
killall SystemUIServer
```

## Other Screenshot Commands
| Command | What it does |
|---------|-------------|
| `/ss` (alias `/repo view_screenshot`) | Copies the latest macOS screenshot to `screenshots/latest.png` for AI viewing |
| `/repo set_screenshots` | Configures macOS to save screenshots to the `screenshots/` folder (the commands above, automated) |
| `/repo cleanup` | Deletes all screenshot images from `screenshots/` except `latest.png`, to free space |

See [`commands.md`](commands.md) for the full command reference and `modules/repo/README.md` for
implementation details.
