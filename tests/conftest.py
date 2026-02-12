from __future__ import annotations

from pathlib import Path

import pytest

from cip_core.server.app import create_app


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def profiles_dir(repo_root: Path) -> Path:
    return repo_root / "profiles"


@pytest.fixture
def app(profiles_dir: Path):
    return create_app(profiles_dir_override=profiles_dir)
