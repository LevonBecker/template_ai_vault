# Claude Module

Wrapper for the Claude Code CLI, allowing use of your Pro/Max subscription through OpenCode.

## Overview

This module routes `/claude` commands directly to the Claude Code CLI (`claude`). Since Claude Code supports OAuth authentication with Pro/Max accounts, you can use your subscription directly without needing an API key.

## Requirements

- Claude Code CLI installed: `npm install -g @anthropic-ai/claude-code`
- Claude Pro or Max subscription (for OAuth access)

## Usage

### Slash Command

```
/claude [arguments...]
```

### CLI (Direct)

```bash
uv run --no-sync python -m modules.claude.route [arguments...]
```

## Examples

### Check Version

```
/claude --version
```

### Run a Prompt

```
/claude "Explain this function"
```

### Interactive Mode

```
/claude
```

### Specify Model

```
/claude --model opus "your prompt here"
```

### With Options

```bash
# Allow Claude to execute commands
/claude --dangerously-skip-permissions "run npm test"

# Use specific model
/claude --model sonnet "refactor this code"

# Resume a previous session
/claude --resume "continue where we left off"
```

## Common Options

| Option | Description |
|--------|-------------|
| `--model <model>` | Select model: opus, sonnet, haiku |
| `--resume` | Resume a previous session |
| `--dangerously-skip-permissions` | Skip permission prompts (use carefully) |
| `--max-tokens <n>` | Maximum output tokens |
| `--no-input` | Exit after completing request (non-interactive) |

## Architecture

```
User → /claude [args]
  ↓
.opencode/command/claude.md
  ↓
modules/claude/route.py
  ↓
claude CLI (system PATH)
```

## Notes

- This passes all arguments directly to the `claude` CLI
- Claude Code handles OAuth authentication automatically
- Your Pro/Max subscription limits still apply
- See `claude --help` for full CLI options
