# AI Vault
Welcome to my personal AI Vault — I'm sharing months of work so others can get the same setup for free.

Every AI conversation we have — research, project planning, personal documentation — is usually locked inside whatever tool or provider we happened to be using that day. Switch tools and we lose our history; switch providers and we start over. AI Vault fixes that: it's a single, private git repo that holds all of our topics, chats, and docs as plain files, so nothing lives inside a vendor's app or account.

Because it's just files in git, we own it outright. It works with almost any AI tool or provider, syncs across every computer or device with a simple push and pull, and nothing about our setup is tied to one company's roadmap. Switch from Claude to a local model to ChatGPT and back — our history, context, and structure come with us every time.

The result: one portable, permanent home for our AI-assisted work, instead of it scattered across a dozen chat histories we don't control.

## Setup
```bash
git clone https://github.com/LevonBecker/template_ai_vault.git ai_vault
cd ai_vault
./setup.sh
```

This creates the Python virtual environment, installs dependencies, and configures repo paths. For AI service authentication and optional CLI tool installs, see [`docs/`](docs/README.md).

## Topics
Our content is organized into `topics/`, nested however makes sense for us — a simple topic can live at the root, like `topics/shopping/`, or nest deeper, like `topics/health/medical/`, with `topics/health/` just being a folder and not a topic itself.

- **Create one**: `/topic new <path> [description]` — e.g. `/topic new health/dental`. This sets up `chats/`, `docs/`, and AI instruction files for that topic.
- **Switch to one**: `/topic <path>` (or `/topic switch <path>`) — this makes it the **active topic**, so we don't need to specify the path again until we switch elsewhere.
- **See what we have**: `/topic list` shows the active topic; `/topic list all` shows the full tree of every topic we've created.
- **Give it context**: we can tell the AI to update a topic's instructions with details it should always know — "this topic is about my medical history, here's my history file" — so every time we activate it, that context plus our chat history and docs are already on hand.

## Chats
Once we're in a topic, `/chat start [title]` begins a new conversation file, or `/chat resume [title]` picks up an existing one. That file becomes the **active chat**, so we can just keep talking without re-running the command.

When we're done, run `/chat end` — this writes the full conversation to that chat's markdown file so nothing is lost. From there we can `/chat start` a fresh conversation, `/clear` to wipe context, or just close whatever AI tool we're using — either way, our work is already saved to disk.

## Our Content
Everything — topics, chats, docs — is saved locally in our own private git repo, so we're never locked into one AI provider or model. Because it's just files, we can switch tools freely while keeping one shared history, and sync that same content across every computer or device with a simple push and pull.

Once we've made changes, run `/push` to commit and push them to our remote; run `/pull` on another machine to bring them down. That's the whole sync story — no special service required, just git.

## Mobile Access
Cloning a git repo to a phone isn't really practical, and the GitHub app isn't built for browsing markdown and CSV. My workaround: a small automation syncs the repo to an iCloud folder, which Obsidian (with a CSV viewer plugin) reads on my phone — free, and I can browse any topic, chat, or doc from anywhere.

Obsidian is just one option — anything that can read a synced folder of markdown/CSV works. Some AI tools solve this differently: Hermes, for example, can run as a Telegram bot so you can chat with your own setup straight from your phone.

## Migrate Data
A good trick for pulling in a chat from a cloud provider like ChatGPT: ask it to output the conversation in markdown format, then paste it into our active topic's chat and tell the AI to ingest it as context. When we run `/chat end`, it gets written to our local `chats/YYYYMMDD_title.md` — saved and available to any AI provider or tool from then on. Handy for capturing a quick chat on the road, then folding it back into the vault once we're home.

## Tested Setups
I've run AI Vault through all of these — pick whichever fits how you like to work:

| Tool | Type | Notes |
|---|---|---|
| VS Code + GitHub Copilot | Editor extension | Cloud providers, full custom command support |
| VS Code + Cline | Editor extension | Also connects to local models |
| Claude Code CLI | Terminal | Full custom command support |
| OpenCode | Terminal (CLI/TUI) | Full custom command support |
| Open Claw | Terminal (CLI/TUI) | Full custom command support |
| Hermes | Terminal (CLI/TUI) | Full custom command support |
| GPT/Codex (via GitHub Copilot) | Editor extension | Custom commands work only through Copilot |
| GPT/Codex (standalone) | — | No custom command support — bring chats in via [Migrate Data](#migrate-data) |

## Learn More
The full setup guide (AI service auth, CLI installs), command reference, and architecture docs live in [`docs/`](docs/README.md).
