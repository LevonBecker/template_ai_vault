# Repo Manager Agent
The repo module handles repository-level operations including git synchronization, iCloud backup, and cleanup tasks.

## Features
- **Repository Push/Pull**: Full git operations and iCloud synchronization
- **Screenshot Cleanup**: Remove old screenshots from centralized repo screenshots/ folder
- **Cross-Device Sync**: Keep work synchronized via git and iCloud Obsidian
- **Automated Commits**: Timestamp-based commit messages
- **Error Handling**: Graceful handling of push/pull failures

## Commands
### `/repo push` (alias: `/push`)
Push changes to git remote and iCloud Obsidian folder from any location.

**Workflow:**
1. **Navigate to repository root** - Automatically changes to repo directory
2. **Git pull** - Fetch and merge latest changes from remote
3. **Check for local changes** - Identify uncommitted work with `git status`
4. **Stage all changes** - Run `git add .` if changes detected
5. **Commit with timestamp** - Create commit: `Push repository: Automated commit YYYY-MM-DD HH:MM:SS`
6. **Push to remote** - Upload changes to GitHub (continues on failure)
7. **Push to iCloud** - Copy content to iCloud Obsidian folder using rsync
8. **Clean up** - Remove any .git folder from iCloud copy
9. **Confirm completion** - Show status summary

**Features:**
- ✅ Works from any directory in the repository
- ✅ Automatic git operations (pull, commit, push)
- ✅ iCloud Obsidian folder synchronization (~700KB)
- ✅ Timestamp-based commit messages
- ✅ Error handling for each push step
- ✅ Cross-device content availability
- ✅ Excludes hidden files from iCloud push

**Rsync Exclusions:**
```
.git
.gitignore
.gitattributes
.DS_Store
.claude
.opencode
.*  (all hidden files)
```

**When to Use:**
- **End of research session** - Push all work before closing
- **After making changes** - Save work to remote and iCloud
- **Before switching devices** - Ensure content is available everywhere
- **Regular backups** - Keep work synchronized and safe
- **After major changes** - Backup important work immediately

**Error Handling:**
- Git pull failure: Stops execution
- Git push failure: Continues with iCloud push (shows warning)
- iCloud push failure: Stops execution with error

**Module:** `modules.repo.push` (via `/repo push`)

### `/repo pull` (alias: `/pull`)
Pull updates from git remote and iCloud Obsidian folder to local repository.

**Workflow:**
1. **Check working directory** - Ensures no uncommitted changes (blocks if dirty)
2. **Force pull active_topic.yml** - Ensures active topic syncs from git remote (ignores local timestamp)
3. **Git pull** - Fetch and merge latest changes from remote
4. **Pull from iCloud** - Copy `topics/` directory from iCloud Obsidian folder to local using rsync
   - Syncs entire `topics/` directory recursively
   - Includes all subdirectories: `chats/`, `docs/`, etc.
   - Includes all file types: `.md`, `.csv`, `.pdf`, images, etc.
5. **Show changes** - Display what changed from iCloud (git status)
6. **Manual review** - User reviews and commits iCloud changes if needed

**Features:**
- ✅ Safe operation (requires clean working directory)
- ✅ Forces `active_topic.yml` from remote (ensures topic sync across devices)
- ✅ Syncs only `topics/` directory from iCloud (not code/config files)
- ✅ Supports all file types in topics (not just markdown)
- ✅ No auto-commit (manual review required)
- ✅ Git + iCloud updates in one command
- ✅ Clear reporting of changes

**iCloud Sync Scope:**
- ✅ `topics/` - Entire directory recursively
  - `topics/health/dental/chats/*.md`
  - `topics/health/dental/docs/*.md`
  - `topics/shopping/electronics/docs/*.csv`
  - `topics/food_and_drink/docs/**/*`
- ❌ Root-level files (code, configs, scripts)
- ❌ Python modules
- ❌ Git files

**When to Use:**
- **Start of research session** - Get latest from git and iCloud
- **After making changes on another device** - Pull updates to local
- **Before starting work** - Ensure you have latest version
- **Cross-device workflow** - Sync active topic and content between computers

**Error Handling:**
- Uncommitted changes: Blocks operation, asks to commit/stash first
- Git pull failure: Stops execution
- iCloud path missing: Warning shown, continues with git-only pull
- Rsync failure: Warning shown, git pull still succeeds

**Module:** `modules.repo.pull` (via `/repo pull`)

### `/repo cleanup`
Clean up old screenshot images from centralized repository screenshots/ folder.

**Workflow:**
1. **Navigate to repository root** - Automatically changes to repo directory
2. **Scan central screenshots/** - Find all image files in `${repo_local}/screenshots/`
3. **Preserve latest.png** - Keep `latest.png` for AI viewing
4. **Count files** - Report total number of screenshot files to be deleted
5. **Calculate size** - Show total disk space to be freed
6. **Delete files** - Remove all screenshot files except `latest.png`
7. **Show git status** - Display files staged for deletion
8. **Suggest next step** - Recommend running `/push` to commit changes

**File Patterns Cleaned:**
```
*.png (except latest.png)
*.jpg
*.jpeg
*.PNG
*.JPG
*.JPEG
```

**Target Directory:**
```
${repo_local}/screenshots/
(Centralized screenshots folder at repo root)
```

**Preserved File:**
```
latest.png - Always kept for AI viewing via 'ss' command
```

**Output Example:**
```
🧹 Starting screenshot cleanup...
🔍 Scanning central screenshots/ folder...
📋 Found 15 screenshot files (excluding latest.png):
./screenshots/Screenshot 2026-01-04 at 3.00.09 PM.png
./screenshots/Screenshot 2026-01-03 at 2.15.22 PM.png
...

📏 Calculating file sizes...
Total size: 2.3 MB

🗑️ Deleting old screenshots...
   Deleted: ./screenshots/Screenshot 2026-01-04 at 3.00.09 PM.png
   Preserved: ./screenshots/latest.png
   ...

✅ Cleanup completed!
   - Files deleted: 14
   - Files preserved: 1 (latest.png)

📊 Git status (deleted files):
 D screenshots/Screenshot 2026-01-04 at 3.00.09 PM.png
   Total files staged for deletion: 14

💡 Next steps:
   Run '/push' to commit and push these changes
```

**Features:**
- ✅ Works from any directory in the repository
- ✅ Scans centralized screenshots/ folder only
- ✅ Preserves `latest.png` for AI viewing
- ✅ Case-insensitive file matching (PNG, png, JPG, jpg)
- ✅ Shows files being deleted
- ✅ Reports total cleanup statistics
- ✅ Stages deletions in git automatically
- ✅ No confirmation required (fast operation)

**Use Cases:**
- **Before major commits** - Reduce repository size
- **Storage management** - Free up disk space
- **Git LFS management** - Clean up tracked files
- **Regular maintenance** - Keep repo lightweight
- **After screenshot-heavy sessions** - Remove temporary visual references while preserving latest.png

**Important Notes:**
- Screenshots are tracked by Git LFS but still consume local space
- Cleanup stages files for deletion but doesn't commit automatically
- Run `/push` after cleanup to commit and push deletions
- `latest.png` is ALWAYS preserved for AI viewing via `ss` command
- No confirmation prompt - deletion is immediate

**Module:** `modules.repo.cleanup` (via `/repo cleanup`)

### `/repo set_screenshots`
Configure macOS to save all screenshots to the central repository `screenshots/` folder.

**Workflow:**
1. Ensure the central `screenshots/` directory exists at the repo root
2. Update macOS screenshot location via `defaults write com.apple.screencapture location`
3. Restart the macOS UI server with `killall SystemUIServer`
4. Confirm the final configured path

**When to Use:**
- After running topic or conversation scripts that point screenshots at per-topic folders
- When screenshots start showing up on Desktop or another unexpected location
- After macOS updates or settings resets that break the central screenshot flow
- Anytime you want to ensure screenshots go to the central repo folder

**Output Example:**
```
🎯 Setting macOS screenshot location to central repo folder
📂 Repository root: ${repo_local}
📸 Ensuring screenshots directory exists...
⚙️ Updating macOS screenshot location...
✅ Screenshot location configured: ${repo_local}/screenshots
💡 All new screenshots will save here. Use 'ss' to view the latest screenshot.
```

**Features:**
- ✅ Creates screenshots folder if it doesn't exist
- ✅ Sets macOS system preference for screenshot location
- ✅ Restarts UI server to apply changes immediately
- ✅ Confirms the configured path
- ✅ Works from any directory

**Use Cases:**
- **After topic initialization** - Topic scripts may change screenshot location
- **Session start** - Ensure screenshots go to central location
- **Troubleshooting** - Fix when screenshots save to wrong location
- **After macOS updates** - Reset if system updates change preferences

**Module:** `modules.repo.set_screenshots` (via `/repo set_screenshots`)

## Feature Branch / PR Workflow
A separate set of commands for a git-flow style feature-branch → Pull Request workflow. These are
independent of `/repo push` and `/repo pull` (which handle the primary tracked branch plus iCloud
sync) — use them when working on a feature branch that needs a GitHub Pull Request.

### `/pr-notes`
Compare the current branch to its detected base branch (`development`/`develop`/`main`/`master`)
and draft a `## Summary` / `## Changes` PR description, saving it to `tmp/pull_requests/`.

**Module:** `modules.repo.pr_diff` + `modules.repo.pr_notes` (via `/pr-notes`)

### `/pr`
Same diff/notes drafting as `/pr-notes`, but opens the Pull Request directly via `gh pr create`
instead of saving notes to a file. Does not push — run `/punch-it-chewy` or `/pr_push` first if the
branch isn't already pushed.

**Module:** `modules.repo.pr_diff` + `modules.repo.pr_create` (via `/pr`)

### `/rebase`
Rebase the current branch onto the remote default branch (`origin/main` or `origin/master`).
Optionally offers to run `/squash` first. Handles stashing local changes and interactive conflict
resolution (ours/theirs/manual) if restoring the stash conflicts.

**Module:** `modules.repo.rebase` (via `/rebase`)

### `/squash`
Anchored squash of every commit down to the repository's root commit into one commit, with an
auto-generated bulleted message. Prompts to review the message, confirm the (irreversible) local
squash, and optionally force-push (`--force-with-lease`).

**Module:** `modules.repo.squash` (via `/squash`)

### `/punch-it-chewy`
Pushes the current feature branch (fix → test → commit → `git push --set-upstream`), then drafts
PR notes and opens the Pull Request — combines `pr_push` + `/pr` in one command.

**Module:** `modules.repo.pr_push` (push step) + `modules.repo.pr_diff` / `modules.repo.pr_create`
(PR step), via `/punch-it-chewy`

## Directory Structure
Repository management affects the entire repository:
```
template_ai_vault/                                  (Git repository)
├── topics/
│   ├── mac/
│   │   └── fusion/
│   │       ├── conversations/
│   │       └── docs/
│   ├── business/
│   │   └── accounting/
│   │       ├── conversations/
│   │       └── docs/
│   └── legal/
│       └── past_record/
│           ├── conversations/
│           └── docs/
├── screenshots/                              (cleaned by /repo cleanup, preserves latest.png)
│   ├── latest.png                           (preserved for AI viewing)
│   └── Screenshot 2026-01-04...png          (removed by cleanup)
├── agents/
│   └── repo/                                (this module)
├── .git/                                    (synced by repo-sync)
└── ...

iCloud/Documents/template_ai_vault/                (iCloud Obsidian)
├── topics/                                  (synced by repo-sync)
├── screenshots/                             (synced by repo-sync)
├── agents/                                  (synced by repo-sync)
└── ...                                      (no .git or hidden files)
```

## Git Integration
### Push/Pull Operations
**Pull Sequence:**
```bash
git status --porcelain                            # Check for uncommitted changes (block if dirty)
git checkout origin/main -- active_topic.yml      # Force pull active topic from remote
git pull                                          # Fetch and merge from remote
rsync ... iCloud/topics/ → local/topics/          # FROM iCloud TO local (topics/ only)
git status                                        # Show changes from iCloud
```

**Push Sequence:**
```bash
git pull                # Fetch and merge from remote
git status --porcelain  # Check for changes
git add .               # Stage all changes
git commit -m "Push repository: Automated commit 2025-12-11 01:30:45"
git push                # Upload to remote
rsync ...               # FROM local TO iCloud
```

**Commit Message Format:**
```
Push repository: Automated commit YYYY-MM-DD HH:MM:SS
```

### Cleanup Operations
**Detection:**
```bash
find . -type f -path "*/screenshots/*" \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" \)
```

**Deletion:**
```bash
rm [screenshot files]
git status --porcelain | grep "^.D"  # Show deleted files
```

Files are staged for deletion but not committed. User must run `/push` to commit.

## iCloud Synchronization
### Rsync Configuration
**Push Command (local → iCloud):**
```bash
rsync -avz --delete \
  --exclude='.git' \
  --exclude='.gitignore' \
  --exclude='.gitattributes' \
  --exclude='.DS_Store' \
  --exclude='.claude' \
  --exclude='.opencode' \
  --exclude='.*' \
  "$REPO_PATH/" "$ICLOUD_PATH"
```

**Pull Command (iCloud → local):**
```bash
# Only sync topics/ directory (includes all subdirectories like docs/, chats/)
rsync -avz --update \
  --exclude='.git' \
  --exclude='.DS_Store' \
  "$ICLOUD_PATH/topics/" "$REPO_PATH/topics"
```

**Options:**
- `-a` - Archive mode (preserves permissions, timestamps)
- `-v` - Verbose output
- `-z` - Compress during transfer
- `--delete` - (Push only) Remove files from iCloud that don't exist in repo
- `--update` - (Pull only) Only copy files that are newer in source

**Pull Scope:**
- ✅ `topics/` - All content, all file types, all subdirectories
- ❌ Root files - Code, configs, scripts not synced from iCloud
- ❌ Python modules - Only tracked in git, not iCloud

**Benefits:**
- Content accessible in Obsidian on all devices
- iOS/iPadOS access via Obsidian mobile app
- Automatic iCloud backup
- No git repository overhead in iCloud
- Clean content-only sync
- Cross-device topic and active chat synchronization

## Configuration
Default settings in `config.yml`:
- `repo_path`: "${repo_local}"
- `icloud_path`: "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/template_ai_vault/"

## Permissions Required
- `git_pull` - Pull from remote repository
- `git_push` - Push to remote repository
- `git_commit` - Create commits
- `git_status` - Check repository status
- `file_sync` - Rsync to iCloud
- `file_delete` - Delete screenshot files
- `directory_access` - Navigate repository directories
- `bash_execute` - Run shell scripts

## Dependencies
- `git` - Version control operations
- `rsync` - iCloud synchronization
- `find` - Locate screenshot files

## Best Practices
1. **Pull/Push Regularly**: Run `/repo pull` at start, `/repo push` at end of sessions
2. **Clean Periodically**: Run `/repo cleanup` when screenshots accumulate
3. **Commit First**: Use `/chat end` for topic work, `/repo push` for repo-level push
4. **Check Status**: Review git status before push if concerned about changes
5. **Verify iCloud**: Occasionally check iCloud Obsidian folder to confirm sync
6. **Network Aware**: Git operations require network connectivity
7. **Backup Important**: Always push before major changes or deletions

## Workflow Examples
**Typical Research Session:**
```
1. /topic switch <path>      # Switch to topic (auto-saves current chat)
2. /chat start <title>       # Begin conversation (auto-ends previous if needed)
   [work on research]
3. /chat end                 # Save conversation (commits topic changes and pushes)
4. /repo push                # Push entire repository to iCloud (if needed)
```

**Cleanup and Push:**
```
1. /repo cleanup             # Remove all screenshots (23 files)
2. /repo push                # Commit deletions and push
```

**Cross-Device Workflow:**
```
Device A:
1. /repo pull                # Pull latest before starting
   [work on content]
2. /repo push                # Push changes to iCloud

Device B (later):
1. /repo pull                # Pull changes from Device A
```

## Related Commands
- `/chat end` - Save conversation and commit topic changes
- `/repo push` - Push all commits to remote and iCloud (alias: `/push`)
- `/topic switch <path>` - Switch between topics with auto-save
- `/repo view_screenshot` - View latest screenshot from central folder (alias: `/ss`)

## Files
- `push.py` - Push to git and iCloud (used by `/repo push`, alias `/push`)
- `pull.py` - Pull from git and iCloud (used by `/repo pull`, alias `/pull`)
- `cleanup.py` - Screenshot cleanup module (used by `/repo cleanup`)
- `set_screenshots.py` - macOS screenshot location configuration module (used by `/repo set_screenshots`)
- `view_screenshot.py` - Copy latest screenshot to latest.png (used by `/repo view_screenshot`, alias `/ss`)
- `config.yml` - Agent configuration
- `README.md` - This file

## Command Aliases
- `/push` → Push to git and iCloud
- `/pull` → Pull from git and iCloud
- `/ss` → View latest screenshot
