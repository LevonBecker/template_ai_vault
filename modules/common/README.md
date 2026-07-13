# Common Utilities Module
Shared utilities and helper functions used across all modules in the template_ai_vault repository.

## Overview
This module provides common functionality that is used by other modules throughout the repository, including configuration parsing and utility functions.

## Modules
### `view_screenshot.py` (moved to repo module)
Screenshot utility lives in `modules/repo/view_screenshot.py`.

**Usage:**
```bash
uv run python -m modules.repo.view_screenshot
```

### `utils.py`
Common utility functions for console output, error handling, and shared operations.

**Functions:**
- `success(message)` - Print success messages with ✅ emoji
- `error(message)` - Print error messages with ❌ emoji  
- `warning(message)` - Print warning messages with ⚠️ emoji
- `info(message)` - Print info messages with ℹ️ emoji

## Dependencies
This module depends on:
- `repo.fetch_properties` - For reading configuration from `properties.yml`
- Standard library: `pathlib`, `shutil`
- Internal CLI helper: `modules/common/cli.py` (TUI-safe prompt/confirm/option handling)

## Configuration
Uses `properties.yml` at repository root:

```yaml
screenshots:
  location: "${repo_local}/screenshots"
  latest_file: "latest.png"
  preserve_files:
    - "latest.png"
  cleanup_patterns:
    - "*.png"
    - "*.jpg"
    - "*.jpeg"
```

## Architecture
The common module follows these principles:
- **Shared utilities only** - Functions used by multiple modules
- **No business logic** - Pure utility functions
- **Minimal dependencies** - Only depends on standard library and config
- **Clear error messages** - User-friendly output with emojis
- **Type hints** - Full type annotations for all functions

## Integration
Other modules import from common:

```python
from modules.common.utils import success, error, warning, info
from modules.repo.view_screenshot import main as copy_latest_screenshot
```

## Testing
Test the screenshot module:

```bash
# Navigate to repo root first
cd $HOME/Development/levonbecker/template_ai_vault

# Run the module
uv run python -m modules.repo.view_screenshot

# Verify latest.png was updated
ls -la screenshots/latest.png
```

## Error Handling
The screenshot module handles:
- Missing screenshots directory
- No screenshots found
- Permission errors
- Invalid file paths

All errors are reported with clear messages and appropriate exit codes.
