# Setup
## 1. Initial Setup
```bash
git clone https://github.com/LevonBecker/template_ai_vault.git ai_vault
cd ai_vault

# macOS or Linux
./setup.sh

# Windows (PowerShell)
.\setup.ps1
```

Both scripts do the same thing: install `uv` (user-local — Homebrew on macOS, the official per-user
installer script on Linux/Windows, no `sudo`/admin needed), create the `.venv` virtual environment,
run `uv sync` to install dependencies, then hand off to Python for everything else:
`uv run --no-sync invoke setup.properties` creates and configures `properties.yml` (see step 2).

`setup.sh` also works as `/setup` once an AI tool is running. It's structured as small functions
(`install_tools_macos` / `install_tools_linux` / `setup_python_env` / `configure_properties`) with a
`main()` that branches on `uname` — see `setup.sh` itself for the exact logic.

**Screenshots are macOS-only.** `/repo set_screenshots` and the `/ss` workflow rely on macOS's
`defaults write com.apple.screencapture` — everything else in the repo works the same on all three
platforms.

## 2. `properties.yml` (automatic)
`properties.yml` at the repo root is the central config every module reads paths from (see
[`architecture.md`](architecture.md#configuration-files)). It's gitignored — machine-specific, never
committed — and generated for you:

- **First run**: `inv setup.properties` creates `properties.yml` from a built-in template, then
  detects and stamps `repo.local` (this repo's actual path on disk) and `repo.remote` (from
  `git remote get-url origin`, if you've forked it).
- **Re-run any time**: `uv run --no-sync invoke setup.properties` — safe and idempotent. Run it again
  after moving the repo on disk, renaming it, or pointing it at a new fork; it just re-stamps the same
  three fields.
- If any module can't find `properties.yml` at all, it raises a clear error telling you to run this
  command — you'll never silently get someone else's paths.

**Not auto-detected** — edit `properties.yml` by hand for these, only if you use the feature:

| Key | What it's for |
|---|---|
| `icloud.enabled` | Turns iCloud sync on for `/push`/`/pull` — **`false` by default**. Set `true` only if you use the iCloud Obsidian mobile workflow (see [Mobile Access](../README.md#mobile-access)) |
| `icloud.path` | Your own iCloud Obsidian vault path — only read when `icloud.enabled: true` |
| `skeleton.local` / `skeleton.remote` | A shared-tooling repo to pull from via `/sync-setup` — leave as-is unless you maintain your own |

`screenshots.location` **is** auto-derived (`<repo.local>/screenshots`) every time `setup.properties`
runs, so don't hand-edit it — it'll get overwritten on the next run.

## 3. AI Service Authentication
If you're using OpenCode:
1. Open opencode
2. `CTRL+P`
3. Connect Provider (`CTRL+A`)

##### Anthropic
1. Pro/Max account
2. Copy/paste the URL to your browser
3. Copy/paste the auth key back into OpenCode

##### GitHub Copilot
1. GitHub account
2. Copy/paste the URL to your browser
3. Copy/paste the auth key
4. Approve

##### OpenAI (ChatGPT)
1. Plus/Pro account
2. Copy/paste the URL to your browser
3. Copy/paste the auth key back into OpenCode

## 4. Optional — Install AI Model CLI Tools
Only needed if you want an agent to shell out to another model's CLI, or if you want to use one of
these tools directly instead of/alongside OpenCode.

#### Anthropic Claude Code
```bash
brew install --cask claude-code
claude auth login
# or: export ANTHROPIC_API_KEY="your_api_key_here"
```

The repo also ships a `/claude` command that proxies straight to this CLI using your Pro/Max
subscription — see `modules/claude/README.md`.

#### GitHub CLI
```bash
brew install gh
gh auth login
```

Required for the PR workflow commands (`/pr`, `/punch-it-chewy`) — they shell out to `gh pr create`.

#### GitHub Copilot CLI
```bash
brew install copilot-cli
# Authenticate with your GitHub CLI account
```

#### Google Gemini CLI
```bash
brew install gemini-cli
gemini auth login
# or: export GEMINI_API_KEY="your_api_key_here"
```

#### OpenAI Codex CLI
```bash
brew install codex
codex  # then select ChatGPT auth
```

#### Persist API keys
Add to `~/.zshrc` or `~/.bash_profile`, then `source` it:
```bash
export ANTHROPIC_API_KEY="your_api_key_here"
export GEMINI_API_KEY="your_api_key_here"
```

## 5. Optional — Local LLM (Ollama)
For fully offline/local model use on Apple Silicon:
```bash
uv run --no-sync invoke ollama.install
```

This is invoke-task-only (no slash command) — see `inv ollama.list` / `inv ollama.status` /
`inv ollama.update` / `inv ollama.uninstall` and `modules/ollama/`.

## 6. Configure Screenshots (macOS)
```bash
uv run --no-sync python -m modules.repo.route "set_screenshots"
# or, once an AI tool is running: /repo set_screenshots
```

Points macOS screenshot captures at the repo's `screenshots/` folder instead of the Desktop. See
[`screenshots.md`](screenshots.md) for the full workflow and the manual `defaults write` commands.

## 7. Verify Setup
```bash
uv run --no-sync python -m modules.topic.list
```

## Next Steps
- [`commands.md`](commands.md) — full command reference
- [`architecture.md`](architecture.md) — how the multi-tool automation is built
- [`custom_prompts.md`](custom_prompts.md) — how to add or modify a slash command
