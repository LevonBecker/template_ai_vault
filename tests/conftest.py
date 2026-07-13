"""Pytest configuration and fixtures."""

import shutil
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_repo(tmp_path):
    """
    Create a temporary repository structure for testing.

    Args:
        tmp_path: Pytest's temporary directory fixture.

    Yields:
        Path to temporary repository.
    """
    repo = tmp_path / "test_repo"
    repo.mkdir()

    # Create topics directory
    topics = repo / "topics"
    topics.mkdir()

    # Create screenshots directory
    screenshots = repo / "screenshots"
    screenshots.mkdir()

    # Create test topic
    test_topic = topics / "test" / "example"
    test_topic.mkdir(parents=True)

    # Create properties.yml
    props = repo / "properties.yml"
    props.write_text(
        f"""---
repo:
  local: "{repo}"
  remote: "github.com/test/test_repo"

icloud:
  path: "{tmp_path}/icloud/"

screenshots:
  location: "{screenshots}"
  latest_file: "latest.png"
  preserve_files:
    - "latest.png"
  cleanup_patterns:
    - "*.png"
    - "*.jpg"
    - "*.jpeg"
"""
    )

    yield repo

    # Cleanup
    if repo.exists():
        shutil.rmtree(repo)


@pytest.fixture
def mock_topic_dir(temp_repo):
    """
    Fixture for a mock topic directory.

    Args:
        temp_repo: Temporary repository fixture.

    Returns:
        Path to mock topic directory.
    """
    topic_dir = temp_repo / "topics" / "test" / "example"
    return topic_dir


@pytest.fixture
def mock_screenshots_dir(temp_repo):
    """
    Fixture for mock screenshots directory.

    Args:
        temp_repo: Temporary repository fixture.

    Returns:
        Path to screenshots directory.
    """
    return temp_repo / "screenshots"
