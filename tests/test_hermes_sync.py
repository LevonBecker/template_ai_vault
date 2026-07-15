"""Tests for modules/hermes/sync.py — parser, classifier, generator."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_prompt(pd: Path, name: str, description: str, body: str, argument_hint: str = "") -> Path:
    """Write a minimal .github/prompts/<name>.prompt.md test fixture."""
    hint_line = f"argument-hint: {argument_hint}\n" if argument_hint else ""
    content = f"---\nname: {name}\ndescription: {description}\n{hint_line}agent: agent\n---\n\n{body}"
    path = pd / f"{name}.prompt.md"
    path.write_text(content, encoding="utf-8")
    return path


def _load_sync_module(prompts_dir: Path, monkeypatch: pytest.MonkeyPatch):
    """Import modules.hermes.sync with REPO_ROOT and PROMPTS_DIR monkeypatched.

    PROMPTS_DIR/REPO_ROOT are computed in modules.common.prompt_commands (the shared
    .prompt.md parser hermes/sync.py delegates to) — both modules must be force-reimported
    together so hermes.sync picks up prompt_commands' freshly patched constants.
    """
    import modules.common.route_utils as ru  # noqa: PLC0415  # pylint: disable=import-outside-toplevel

    repo = prompts_dir.parent.parent  # tmp_path root acts as repo root
    monkeypatch.setattr(ru, "find_repo_root", lambda: repo)

    # Force reimport so module-level constants pick up patched find_repo_root
    for mod_name in ("modules.hermes.sync", "modules.common.prompt_commands"):
        if mod_name in sys.modules:
            del sys.modules[mod_name]

    import modules.common.prompt_commands as prompt_commands_mod  # noqa: PLC0415  # pylint: disable=import-outside-toplevel
    import modules.hermes.sync as sync_mod  # noqa: PLC0415  # pylint: disable=import-outside-toplevel

    monkeypatch.setattr(prompt_commands_mod, "REPO_ROOT", repo)
    monkeypatch.setattr(prompt_commands_mod, "PROMPTS_DIR", prompts_dir)
    monkeypatch.setattr(sync_mod, "REPO_ROOT", repo)
    return sync_mod


@pytest.fixture
def prompts_dir(tmp_path: Path) -> Path:
    """Create a temp .github/prompts directory."""
    pd = tmp_path / ".github" / "prompts"
    pd.mkdir(parents=True)
    return pd


# ---------------------------------------------------------------------------
# PromptCommand parser tests
# ---------------------------------------------------------------------------


class TestPromptCommandParser:
    """Tests for PromptCommand parsing and classification."""

    def test_exec_no_args_classified_exec(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(prompts_dir, "pull", "Pull from git", '!`uv run --no-sync python -m modules.repo.route "pull"`')
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        assert len(cmds) == 1
        assert cmds[0].classification == "exec"
        assert cmds[0].r_name == "r-pull"
        assert cmds[0].description == "Pull from git"

    def test_arg_style_classified_arg(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(
            prompts_dir, "topic", "Manage topics", '!`uv run --no-sync python -m modules.topic.route "$ARGUMENTS"`'
        )
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        assert cmds[0].classification == "arg"

    def test_ai_guided_no_exec_line(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(prompts_dir, "add_expense", "Add expense", "Collect vendor, amount, description from user.")
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        assert cmds[0].classification == "ai_guided"

    def test_long_running_test_classified_exec_long(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(prompts_dir, "test", "Run tests", "!`uv run --no-sync invoke test`")
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        assert cmds[0].classification == "exec_long"

    def test_long_running_upgrade_classified_exec_long(
        self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _write_prompt(prompts_dir, "upgrade", "Upgrade deps", "!`uv run --no-sync invoke upgrade`")
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        assert cmds[0].classification == "exec_long"

    def test_r_name_uses_slug_with_hyphens(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(
            prompts_dir,
            "add-expense",
            "Add expense",
            '!`uv run --no-sync python -m modules.example.route "add_expense"`',
        )
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        assert cmds[0].r_name == "r-add-expense"

    def test_description_parsed_from_frontmatter(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(
            prompts_dir,
            "ss",
            "View the latest screenshot",
            '!`uv run --no-sync python -m modules.repo.route "view_screenshot"`',
        )
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        assert cmds[0].description == "View the latest screenshot"

    def test_argument_hint_parsed(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(
            prompts_dir,
            "chat",
            "Manage chats",
            '!`uv run --no-sync python -m modules.chat.route "$ARGUMENTS"`',
            argument_hint="start [title] | end | list",
        )
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        assert cmds[0].argument_hint == "start [title] | end | list"

    def test_claude_command_skipped(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(prompts_dir, "claude", "Run Claude CLI", "!`claude`")
        _write_prompt(prompts_dir, "pull", "Pull", '!`uv run --no-sync python -m modules.repo.route "pull"`')
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        names = [c.name for c in cmds]
        assert "claude" not in names
        assert "pull" in names

    def test_deduplication_keeps_first_alphabetically(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """list-expenses and list_expenses deduplicate — only one entry kept."""
        _write_prompt(
            prompts_dir,
            "list_expenses",
            "List expenses",
            '!`uv run --no-sync python -m modules.example.route "list_expenses"`',
        )
        # Hyphenated duplicate
        (prompts_dir / "list-expenses.prompt.md").write_text(
            "---\nname: list-expenses\ndescription: List expenses\nagent: agent\n---\n\n"
            '!`uv run --no-sync python -m modules.example.route "list_expenses"`',
            encoding="utf-8",
        )
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        names = [c.name for c in cmds]
        assert names.count("list_expenses") == 1


# ---------------------------------------------------------------------------
# quick_commands generator tests
# ---------------------------------------------------------------------------


class TestQuickCommandsGenerator:
    """Tests for generate_quick_commands()."""

    def test_only_exec_commands_included(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(prompts_dir, "pull", "Pull", '!`uv run --no-sync python -m modules.repo.route "pull"`')
        _write_prompt(prompts_dir, "topic", "Topics", '!`uv run --no-sync python -m modules.topic.route "$ARGUMENTS"`')
        _write_prompt(prompts_dir, "add_expense", "Expense", "AI guided, no exec")
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        qc = sync.generate_quick_commands(cmds)
        assert "r-pull" in qc
        assert "r-topic" not in qc
        assert "r-add_expense" not in qc

    def test_exec_long_not_in_quick_commands(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(prompts_dir, "test", "Run tests", "!`uv run --no-sync invoke test`")
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        qc = sync.generate_quick_commands(cmds)
        assert "r-test" not in qc

    def test_quick_command_entry_has_type_and_command(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(
            prompts_dir, "ss", "Screenshot", '!`uv run --no-sync python -m modules.repo.route "view_screenshot"`'
        )
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        qc = sync.generate_quick_commands(cmds)
        assert qc["r-ss"]["type"] == "exec"
        assert "command" in qc["r-ss"]
        assert "uv run --no-sync" in qc["r-ss"]["command"]

    def test_exec_override_applied_for_fix(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(prompts_dir, "fix", "Run fixes", "!`uv run --no-sync invoke fix`")
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        qc = sync.generate_quick_commands(cmds)
        assert "r-fix" in qc
        assert "invoke fix" in qc["r-fix"]["command"]

    def test_command_prefixed_with_cd_repo_root(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(prompts_dir, "pull", "Pull", '!`uv run --no-sync python -m modules.repo.route "pull"`')
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        qc = sync.generate_quick_commands(cmds)
        assert qc["r-pull"]["command"].startswith("cd ")


# ---------------------------------------------------------------------------
# SKILL.md generator tests
# ---------------------------------------------------------------------------


class TestSkillMdGenerator:
    """Tests for generate_skill_md()."""

    def test_skill_header_contains_name_and_auto_generated(
        self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _write_prompt(prompts_dir, "pull", "Pull", '!`uv run --no-sync python -m modules.repo.route "pull"`')
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        md = sync.generate_skill_md(cmds)
        assert "name: r-research" in md
        assert "AUTO-GENERATED" in md

    def test_exec_commands_appear_in_table(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(prompts_dir, "pull", "Pull from git", '!`uv run --no-sync python -m modules.repo.route "pull"`')
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        md = sync.generate_skill_md(cmds)
        assert "/r-pull" in md
        assert "Pull from git" in md
        assert "Zero-Token Quick Commands" in md

    def test_arg_commands_have_subsection(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(
            prompts_dir, "topic", "Manage topics", '!`uv run --no-sync python -m modules.topic.route "$ARGUMENTS"`'
        )
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        md = sync.generate_skill_md(cmds)
        assert "### `/r-topic`" in md
        assert "AI-Routed Commands" in md

    def test_ai_guided_commands_in_workflow_section(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(prompts_dir, "add_expense", "Add expense", "Collect vendor from user first.")
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        md = sync.generate_skill_md(cmds)
        assert "AI-Guided Workflows" in md
        assert "/r-add_expense" in md

    def test_long_running_commands_in_long_section(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(prompts_dir, "test", "Run tests", "!`uv run --no-sync invoke test`")
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        md = sync.generate_skill_md(cmds)
        assert "Long-Running" in md
        assert "/r-test" in md

    def test_ss_vision_note_always_present(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(prompts_dir, "pull", "Pull", '!`uv run --no-sync python -m modules.repo.route "pull"`')
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        md = sync.generate_skill_md(cmds)
        assert "vision_analyze" in md
        assert "Two Steps" in md

    def test_footer_contains_regen_instruction(self, prompts_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_prompt(prompts_dir, "pull", "Pull", '!`uv run --no-sync python -m modules.repo.route "pull"`')
        sync = _load_sync_module(prompts_dir, monkeypatch)
        cmds = sync.load_commands()
        md = sync.generate_skill_md(cmds)
        assert "hermes.sync" in md
