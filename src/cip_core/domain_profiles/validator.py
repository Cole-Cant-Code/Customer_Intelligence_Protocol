"""Validation helpers for profile payloads and YAML documents."""

from __future__ import annotations

from typing import Any

import yaml
from pydantic import ValidationError

from cip_core.domain_profiles.models import DomainProfile


def validate_profile_payload(
    payload: dict[str, Any],
) -> tuple[bool, list[str], DomainProfile | None]:
    """Validate a loaded profile payload and return rich error details."""
    try:
        profile = DomainProfile.model_validate(payload)
    except ValidationError as exc:
        errors = [
            f"{'.'.join(str(part) for part in err['loc'])}: {err['msg']}"
            for err in exc.errors()
        ]
        return False, errors, None

    return True, [], profile



def validate_profile_yaml(profile_yaml: str) -> tuple[bool, list[str], DomainProfile | None]:
    """Validate profile YAML text against canonical contract."""
    try:
        payload = yaml.safe_load(profile_yaml)
    except yaml.YAMLError as exc:
        return False, [f"yaml: {exc}"], None

    if not isinstance(payload, dict):
        return False, ["root: profile YAML must be a mapping"], None

    return validate_profile_payload(payload)
