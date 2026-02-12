"""Shared constants for domain profile validation."""

from __future__ import annotations

RESERVED_DOMAIN_NAMES = frozenset(
    {
        "healthcare",
        "finance",
        "cyber",
        "climate",
        "legal",
        "military",
        "social",
    }
)

ALLOWED_HIERARCHY_LEVELS = frozenset({"Micro", "Meso", "Macro", "Meta"})

ALLOWED_KERNEL_TYPES = frozenset(
    {
        "exponential",
        "linear",
        "logistic",
        "s_curve",
        "power_law",
        "oscillatory",
        "memory",
    }
)
