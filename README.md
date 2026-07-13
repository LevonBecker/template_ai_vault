# AI Assistant
Welcome to my personal AI Assistant setup that I thought I'd share and maybe help others out.

It's an agnostic AI tool for doing your personal and/or business research, project organization, and documentation — a central repository or place for all of your AI content. It can be used with almost any AI tool or provider.

I usually use VSCode with AI extensions with cloud providers, but also use Cline to connect local models too. I started it with OpenCode, but then Claude turned off support, so I moved back to VSCode, since Claude is king for coding at the moment. I dabbled in Hermes, but again no Claude besides through a GitHub Copilot subscription that runs out too fast.

The biggest win: everything is saved locally as markdown and CSV in a single git repo, so you're never locked into one AI provider or model — switch freely while keeping one shared history, and sync that same context across every computer or device just by pushing and pulling git.

I do have it automated to update an iCloud folder where my Obsidian app pulls its vault from. Then with a csv viewer extension I can view my .md and .csv on my phone anywhere for free.

It isn't locked to any single tool or interface. Use it from VS Code with extensions like GitHub Copilot and Cline, or skip the editor entirely and work from the terminal with CLI/TUI AI tools like OpenCode, the Claude Code CLI, or Hermes — the same topic structure, custom slash commands, and chat history work identically everywhere. That flexibility is the point: switch between AI providers and models freely, because nothing about your setup is tied to a specific one.

Everything is organized into `topics/` — nested however makes sense for you, one folder per project or area of your life — and every conversation gets saved as markdown in that topic's `chats/` folder, alongside whatever docs and CSVs you're tracking. Because it's all just files in a git repo, you resume any conversation exactly where you left off, hand that same context to a different AI tool without re-explaining anything, and sync your entire workspace across every computer or device with a simple push and pull.

A good trick to migrate data from a cloud provider like say ChatGPT: ask it to output the chat in Markdown format. Then copy/paste it to your active topic and chat in your AI Assistant and tell it to ingest this context into the current chat... then when you run /chat end it'll write the context to your local `chats/YYYYMMDD_title.md` and it'll be saved and available for any AI provider or tool to access. I'm sure there are better ways to dump and import if doing a large number of chats, and I'm sure AI can help you with that. I just use it like if I'm on the road and need a quick chat about something and use say ChatGPT. Then I get home, grab that context, and import it to my AI Assistant so I can continue the conversation or at least have it saved.

The result is a single, portable home for your AI-assisted work — one you fully own, that works with whichever AI tool you reach for today and whichever one you switch to tomorrow.

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
