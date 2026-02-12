from __future__ import annotations

import pytest

from cip_core.domain_profiles.loader import load_profile_file
from cip_core.domain_profiles.registry import DomainProfileRegistry


def test_registry_loads_profile_directory(profiles_dir) -> None:
    registry = DomainProfileRegistry.from_directory(profiles_dir)
    assert len(registry) == 1
    descriptor = registry.list()[0]
    assert descriptor["domain_name"] == "customer_signal_core"


def test_registry_rejects_duplicate_registration(profiles_dir) -> None:
    profile_path = profiles_dir / "customer_signal_core.v1.yaml"
    profile = load_profile_file(profile_path)

    registry = DomainProfileRegistry([profile])
    with pytest.raises(ValueError, match="already registered"):
        registry.register(profile)


def test_registry_get_unknown_profile_raises(profiles_dir) -> None:
    registry = DomainProfileRegistry.from_directory(profiles_dir)
    with pytest.raises(KeyError):
        registry.get("does_not_exist")
