"""Profile loading utilities for YAML contracts."""

from __future__ import annotations

from pathlib import Path

import yaml

from cip_core.domain_profiles.models import DomainProfile
from cip_core.domain_profiles.validator import validate_profile_payload


def load_profile_yaml(profile_yaml: str) -> DomainProfile:
    """Load and validate profile YAML string."""
    payload = yaml.safe_load(profile_yaml)
    if not isinstance(payload, dict):
        raise ValueError("profile YAML root must be a mapping")

    ok, errors, profile = validate_profile_payload(payload)
    if not ok or profile is None:
        raise ValueError("; ".join(errors))
    return profile



def load_profile_file(path: Path) -> DomainProfile:
    """Load one profile from disk."""
    text = path.read_text(encoding="utf-8")
    return load_profile_yaml(text)



def load_profiles_from_directory(directory: Path) -> list[DomainProfile]:
    """Load all profile YAML files from a directory recursively."""
    if not directory.exists():
        return []

    profiles: list[DomainProfile] = []
    for path in sorted(directory.rglob("*.yaml")):
        if path.name.startswith("_"):
            continue
        if "schema" in path.name:
            continue
        profiles.append(load_profile_file(path))

    return profiles
