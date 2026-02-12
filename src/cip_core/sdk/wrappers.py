"""SDK wrapper functions for safe profile-based detection."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any, Literal

from cip_core.domain_profiles.registry import DomainProfileRegistry
from cip_core.mantic.runtime import run_detection
from cip_core.sdk.translator import DomainTranslator


def load_registry(profiles_dir: str | Path) -> DomainProfileRegistry:
    """Load profile registry from a directory path."""
    return DomainProfileRegistry.from_directory(Path(profiles_dir))



def safe_detect(
    registry: DomainProfileRegistry,
    profile_name: str,
    layer_values: list[float],
    mode: Literal["friction", "emergence"],
    f_time: float = 1.0,
    threshold_override: dict[str, float] | None = None,
    temporal_config: dict[str, Any] | None = None,
    interaction_mode: Literal["dynamic", "base"] = "dynamic",
    interaction_override: dict[str, float] | list[float] | None = None,
    interaction_override_mode: Literal["scale", "replace"] = "scale",
) -> dict[str, Any]:
    """Run detection against a registered domain profile."""
    profile = registry.get(profile_name)
    return run_detection(
        profile=profile,
        layer_values=layer_values,
        mode=mode,
        f_time=f_time,
        threshold_override=threshold_override,
        temporal_config=temporal_config,
        interaction_mode=interaction_mode,
        interaction_override=interaction_override,
        interaction_override_mode=interaction_override_mode,
    )



def detect_from_translator(
    registry: DomainProfileRegistry,
    profile_name: str,
    translator: DomainTranslator,
    raw_context: Mapping[str, Any],
    mode: Literal["friction", "emergence"],
    f_time: float = 1.0,
    threshold_override: dict[str, float] | None = None,
    temporal_config: dict[str, Any] | None = None,
    interaction_mode: Literal["dynamic", "base"] = "dynamic",
    interaction_override: dict[str, float] | list[float] | None = None,
    interaction_override_mode: Literal["scale", "replace"] = "scale",
) -> dict[str, Any]:
    """Translate raw context through domain adapter then run safe detection."""
    translation = translator.translate(raw_context)
    return safe_detect(
        registry=registry,
        profile_name=profile_name,
        layer_values=translation.layer_values,
        mode=mode,
        f_time=f_time,
        threshold_override=threshold_override,
        temporal_config=temporal_config,
        interaction_mode=interaction_mode,
        interaction_override=interaction_override,
        interaction_override_mode=interaction_override_mode,
    )
