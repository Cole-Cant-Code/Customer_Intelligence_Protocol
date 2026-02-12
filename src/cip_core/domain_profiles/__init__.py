"""Domain profile contract and registry."""

from cip_core.domain_profiles.loader import (
    load_profile_file,
    load_profile_yaml,
    load_profiles_from_directory,
)
from cip_core.domain_profiles.models import DomainProfile
from cip_core.domain_profiles.registry import DomainProfileRegistry
from cip_core.domain_profiles.validator import validate_profile_payload, validate_profile_yaml

__all__ = [
    "DomainProfile",
    "DomainProfileRegistry",
    "load_profile_file",
    "load_profile_yaml",
    "load_profiles_from_directory",
    "validate_profile_payload",
    "validate_profile_yaml",
]
