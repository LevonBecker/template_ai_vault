"""Tests for modules.template.push repo-name rewriting and change classification."""

from pathlib import Path

from modules.common.properties import get_repo_local, get_template_local
from modules.template.push import _classify, rewrite_repo_references


def _configured_names() -> tuple[str, str]:
    """Repo and template names exactly as run_apply derives them from properties.yml."""
    return get_repo_local().name, get_template_local().name


def test_replaces_configured_repo_name_with_template_name():
    repo_name, template_name = _configured_names()
    content = f"path is $HOME/Development/example/{repo_name}/screenshots"
    result = rewrite_repo_references(content, repo_name, template_name)
    assert result == f"path is $HOME/Development/example/{template_name}/screenshots"


def test_existing_template_name_untouched():
    repo_name, template_name = _configured_names()
    content = f"clone {template_name} next to {repo_name}"
    result = rewrite_repo_references(content, repo_name, template_name)
    assert result == f"clone {template_name} next to {template_name}"


def test_multiple_occurrences():
    repo_name, template_name = _configured_names()
    content = f"{repo_name} and {repo_name}, plus {template_name}"
    result = rewrite_repo_references(content, repo_name, template_name)
    assert result == f"{template_name} and {template_name}, plus {template_name}"


def test_substring_containment_is_safe():
    content = "clone template_my_vault next to my_vault"
    result = rewrite_repo_references(content, "my_vault", "template_my_vault")
    assert result == "clone template_my_vault next to template_my_vault"


def test_noop_when_names_match():
    content = "my_vault stays put"
    assert rewrite_repo_references(content, "my_vault", "my_vault") == content


def test_noop_when_repo_name_absent():
    content = "nothing to see here"
    result = rewrite_repo_references(content, "my_vault", "template_my_vault")
    assert result == content


def _write(root: Path, rel: str, content: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_classify_added_modified_deleted(tmp_path):
    repo = tmp_path / "my_vault"
    template = tmp_path / "template_my_vault"

    _write(repo, ".claude/commands/update.md", "brand new command")
    _write(repo, "modules/common/utils.py", "new content")
    _write(repo, "modules/common/shared.py", "same everywhere")
    _write(template, "modules/common/shared.py", "same everywhere")
    _write(template, "modules/common/utils.py", "old content")
    _write(template, ".claude/commands/version.md", "deprecated command")

    added, modified, deleted = _classify(repo, template, "my_vault", "template_my_vault")

    assert added == [Path(".claude/commands/update.md")]
    assert modified == [Path("modules/common/utils.py")]
    assert deleted == [Path(".claude/commands/version.md")]


def test_classify_name_only_difference_not_modified(tmp_path):
    repo = tmp_path / "my_vault"
    template = tmp_path / "template_my_vault"

    _write(repo, "modules/common/utils.py", "path is my_vault/screenshots")
    _write(template, "modules/common/utils.py", "path is template_my_vault/screenshots")

    added, modified, deleted = _classify(repo, template, "my_vault", "template_my_vault")

    assert not added
    assert not modified
    assert not deleted


def test_classify_excluded_template_files_not_deletion_candidates(tmp_path):
    repo = tmp_path / "my_vault"
    template = tmp_path / "template_my_vault"

    _write(repo, "modules/common/utils.py", "content")
    _write(template, "modules/common/utils.py", "content")
    _write(template, "modules/fireball/route.py", "business module stays untouched")

    _, _, deleted = _classify(repo, template, "my_vault", "template_my_vault")

    assert not deleted
