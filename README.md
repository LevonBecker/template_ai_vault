# AI Vault
Welcome to my personal AI Vault setup — I'm sharing it so others can keep their AI content local, secure, and free from provider lock-in.

It's an agnostic AI tool for doing our personal and/or business research, project organization, and documentation — a central repository or place for all of our AI content. It can be used with almost any AI tool or provider.

I usually use VSCode with AI extensions with cloud providers, but also use Cline to connect local models too. I started it with OpenCode, but then Claude turned off support, so I moved back to VSCode, since Claude is king for coding at the moment. I dabbled in Hermes, but again no Claude besides through a GitHub Copilot subscription that runs out too fast.

The biggest win: everything is saved locally in our own private git repo, so we're never locked into one AI provider or model — we can switch freely while keeping one shared history. Our content stays private, yet still syncs across every computer or device just by pushing and pulling git.

I do have it automated to update an iCloud folder where my Obsidian app pulls its vault from. Then with a csv viewer extension I can view my .md and .csv on my phone anywhere for free.

It isn't locked to any single tool or interface. We can use it from VS Code with extensions like GitHub Copilot and Cline, or skip the editor entirely and work from the terminal with CLI/TUI AI tools like OpenCode, the Claude Code CLI, Open Claw, or Hermes — the same topic structure, custom slash commands, and chat history work identically everywhere. The one exception is GPT/Codex, which doesn't support custom prompts or commands on its own — unless we're running it through GitHub Copilot, which does. Otherwise, we can still bring our content in by importing context from an OpenAI chat, or manually pointing it at a prompt file. That flexibility is the point: we can switch between AI providers and models freely, because nothing about our setup is tied to a specific one.

Our content is organized into `topics/`, which supports nesting however makes sense for us. A simple topic can live at the root, like `topics/shopping/`, with subfolders for docs or categories as needed. We can also nest deeper: `topics/health/` can just be a folder — not a topic itself — while `topics/health/medical/` is the actual topic, organizing chats and docs around our medical history, visits, and providers, with subfolders in `docs/` as needed. We can even tell it to update that topic's AI config with context — "this topic is about my personal medical information, here's my history file" — so every time we activate the topic, it already knows our information and has our chat history and docs on hand for whatever we ask next. To create a new topic, run `/topic new guitar` or `/topic new business/accounting/bookkeeping` — the last segment in the path becomes the topic. To switch to (activate) an existing topic, run `/topic health/medical`.

Once we've created or activated a topic, we can start or resume a chat within it. When we're done, run `/chat end`, which tells the AI to pull whatever's in context and write it to the chat log. From there we can `/clear` and start fresh to move on to our next task.

A good trick to migrate data from a cloud provider like say ChatGPT: ask it to output the chat in Markdown format. Then copy/paste it to our active topic and chat in our AI assistant and tell it to ingest this context into the current chat... then when we run `/chat end` it'll write the context to our local `chats/YYYYMMDD_title.md` and it'll be saved and available for any AI provider or tool to access. I'm sure there are better ways to dump and import if doing a large number of chats, and I'm sure AI can help with that. I just use it like if I'm on the road and need a quick chat about something and use say ChatGPT. Then I get home, grab that context, and import it to my AI Vault so I can continue the conversation or at least have it saved.

The result is a single, portable home for our AI-assisted work — one we fully own, that works with whichever AI tool we reach for today and whichever one we switch to tomorrow.

## Setup
```bash
./setup.sh
```

This creates the Python virtual environment, installs dependencies, and configures repo paths. For AI service authentication and optional CLI tool installs, see [`docs/`](docs/README.md).

## Topics
A **topic** is a folder under `topics/` for one project or area of your life — as flat or as nested as you want. `travel/` can stand alone; `health/` can hold `health/dental/`, `health/vision/`, and so on underneath it.

- **Create one**: `/topic new <path> [description]` — e.g. `/topic new health/dental`. This sets up `chats/`, `docs/`, and AI instruction files for that topic.
- **Switch to one**: `/topic <path>` (or `/topic switch <path>`) — this makes it the **active topic**, so you don't need to specify the path again until you switch elsewhere.
- **See what you have**: `/topic list` shows the active topic; `/topic list all` shows the full tree of every topic you've created.

## Chats
Once you're in a topic, `/chat start [title]` begins a new conversation file, or `/chat resume [title]` picks up an existing one. That file becomes the **active chat**, so you can just keep talking without re-running the command.

When you're done, run `/chat end` — this writes the full conversation to that chat's markdown file so nothing is lost. From there you can `/chat start` a fresh conversation, or just close whatever AI tool you're using — either way, your work is already saved to disk.

## Repo Management
Everything you do — new topics, chat logs, docs — is just files in a normal git repo. Once you've made changes, run `/push` to commit and push them to your remote; run `/pull` on another machine to bring them down. That's the whole sync story — no special service required, just git.

## Learn More
The full setup guide (AI service auth, CLI installs), command reference, and architecture docs live in [`docs/`](docs/README.md).
