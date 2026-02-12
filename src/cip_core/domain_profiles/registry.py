"""In-memory domain profile registry."""

from __future__ import annotations

from pathlib import Path

from cip_core.domain_profiles.loader import load_profiles_from_directory
from cip_core.domain_profiles.models import DomainProfile


class DomainProfileRegistry:
    """Registry for validated domain profiles."""

    def __init__(self, profiles: list[DomainProfile] | None = None) -> None:
        self._profiles: dict[str, DomainProfile] = {}
        for profile in profiles or []:
            self.register(profile)

    @classmethod
    def from_directory(cls, directory: Path) -> DomainProfileRegistry:
        """Create registry from profile directory."""
        return cls(load_profiles_from_directory(directory))

    def register(self, profile: DomainProfile) -> None:
        """Register a profile by domain_name."""
        if profile.domain_name in self._profiles:
            raise ValueError(f"Profile '{profile.domain_name}' already registered")
        self._profiles[profile.domain_name] = profile

    def get(self, domain_name: str) -> DomainProfile:
        """Return a profile or raise KeyError."""
        if domain_name not in self._profiles:
            raise KeyError(
                f"Unknown domain profile '{domain_name}'. Available: {sorted(self._profiles)}"
            )
        return self._profiles[domain_name]

    def list(self) -> list[dict[str, object]]:
        """Return profile descriptors for discovery tools."""
        return [self._profiles[name].descriptor() for name in sorted(self._profiles)]

    def __len__(self) -> int:
        return len(self._profiles)
