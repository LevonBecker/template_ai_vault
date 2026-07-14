# Setup
## 1. Initial Setup
```bash
git clone https://github.com/LevonBecker/template_ai_vault.git ai_vault
cd ai_vault
./setup.sh
```

`./setup.sh` (also available as `/setup` once an AI tool is running) creates the Python virtual
environment, installs dependencies, sets up the test automation tasks, and configures repository
properties (`properties.yml`).

## 2. AI Service Authentication
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

## 3. Optional — Install AI Model CLI Tools
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

## 4. Optional — Local LLM (Ollama)
For fully offline/local model use on Apple Silicon:
```bash
uv run --no-sync invoke ollama.install
```

This is invoke-task-only (no slash command) — see `inv ollama.list` / `inv ollama.status` /
`inv ollama.update` / `inv ollama.uninstall` and `modules/ollama/`.

## 5. Configure Screenshots (macOS)
```bash
uv run --no-sync python -m modules.repo.route "set_screenshots"
# or, once an AI tool is running: /repo set_screenshots
```

Points macOS screenshot captures at the repo's `screenshots/` folder instead of the Desktop. See
[`screenshots.md`](screenshots.md) for the full workflow and the manual `defaults write` commands.

## 6. Verify Setup
```bash
uv run --no-sync python -m modules.topic.list
```

## Next Steps
- [`commands.md`](commands.md) — full command reference
- [`architecture.md`](architecture.md) — how the multi-tool automation is built
- [`custom_prompts.md`](custom_prompts.md) — how to add or modify a slash command
