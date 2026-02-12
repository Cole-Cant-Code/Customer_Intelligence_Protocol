"""Safe runtime wrappers around mantic_thinking generic_detect."""

from __future__ import annotations

from typing import Any, Literal

from cip_core.domain_profiles.models import DomainProfile
from cip_core.models.responses import AuditSummary, DetectionEnvelope


def _validate_layer_values(layer_values: list[float], layer_count: int) -> list[float]:
    if len(layer_values) != layer_count:
        raise ValueError(
            "layer_values length "
            f"({len(layer_values)}) must match profile layer count ({layer_count})"
        )

    converted: list[float] = []
    for idx, raw in enumerate(layer_values):
        try:
            value = float(raw)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"layer_values[{idx}] must be numeric") from exc
        converted.append(min(1.0, max(0.0, value)))

    return converted



def _enforce_temporal_allowlist(
    profile: DomainProfile,
    temporal_config: dict[str, Any] | None,
) -> None:
    if not temporal_config:
        return
    kernel = temporal_config.get("kernel_type")
    if kernel and kernel not in profile.temporal_allowlist:
        raise ValueError(
            f"kernel_type '{kernel}' is not allowed for domain '{profile.domain_name}'. "
            f"Allowed: {profile.temporal_allowlist}"
        )

def _extract_clamped_fields(overrides_applied: dict[str, Any]) -> list[str]:
    fields: list[str] = []

    threshold_meta = overrides_applied.get("threshold_overrides")
    if isinstance(threshold_meta, dict) and threshold_meta.get("clamped"):
        fields.append("threshold_overrides")

    temporal_meta = overrides_applied.get("temporal_config")
    if isinstance(temporal_meta, dict):
        clamped = temporal_meta.get("clamped")
        if isinstance(clamped, dict):
            for key in clamped:
                fields.append(f"temporal_config.{key}")

    f_time_meta = overrides_applied.get("f_time")
    if isinstance(f_time_meta, dict) and f_time_meta.get("clamped"):
        fields.append("f_time")

    interaction_meta = overrides_applied.get("interaction")
    if isinstance(interaction_meta, dict):
        clamped = interaction_meta.get("clamped")
        if isinstance(clamped, dict):
            for key in clamped:
                fields.append(f"interaction.{key}")

    return sorted(set(fields))



def _extract_rejected_fields(overrides_applied: dict[str, Any]) -> list[str]:
    fields: list[str] = []

    temporal_meta = overrides_applied.get("temporal_config")
    if isinstance(temporal_meta, dict):
        rejected = temporal_meta.get("rejected")
        if isinstance(rejected, dict):
            for key in rejected:
                fields.append(f"temporal_config.{key}")

    interaction_meta = overrides_applied.get("interaction")
    if isinstance(interaction_meta, dict):
        rejected = interaction_meta.get("rejected")
        if isinstance(rejected, dict):
            for key in rejected:
                fields.append(f"interaction.{key}")

    threshold_meta = overrides_applied.get("threshold_overrides")
    if isinstance(threshold_meta, dict):
        ignored_keys = threshold_meta.get("ignored_keys")
        if isinstance(ignored_keys, list):
            for key in ignored_keys:
                fields.append(f"threshold_override.{key}")

    return sorted(set(fields))



def run_detection(
    profile: DomainProfile,
    layer_values: list[float],
    mode: Literal["friction", "emergence"],
    f_time: float = 1.0,
    threshold_override: dict[str, float] | None = None,
    temporal_config: dict[str, Any] | None = None,
    interaction_mode: Literal["dynamic", "base"] = "dynamic",
    interaction_override: dict[str, float] | list[float] | None = None,
    interaction_override_mode: Literal["scale", "replace"] = "scale",
) -> dict[str, Any]:
    """Run constrained Mantic detection and return normalized envelope."""
    if mode not in {"friction", "emergence"}:
        raise ValueError("mode must be 'friction' or 'emergence'")

    normalized_values = _validate_layer_values(layer_values, len(profile.layer_names))
    _enforce_temporal_allowlist(profile, temporal_config)

    try:
        from mantic_thinking.tools.generic_detect import detect
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("mantic-thinking is not installed") from exc

    result = detect(
        domain_name=profile.domain_name,
        layer_names=profile.layer_names,
        weights=profile.weights,
        layer_values=normalized_values,
        mode=mode,
        f_time=f_time,
        threshold_override=threshold_override,
        temporal_config=temporal_config,
        interaction_mode=interaction_mode,
        interaction_override=interaction_override,
        interaction_override_mode=interaction_override_mode,
        layer_hierarchy=profile.hierarchy,
        detection_threshold=profile.detection_threshold,
    )

    overrides_applied = result.get("overrides_applied") or {}
    audit = AuditSummary(
        overrides_applied=overrides_applied,
        clamped_fields=_extract_clamped_fields(overrides_applied),
        rejected_fields=_extract_rejected_fields(overrides_applied),
        calibration=result.get("calibration") or {
            "domain_name": profile.domain_name,
            "mode": mode,
            "source": "cip-mantic-core",
        },
    )

    envelope = DetectionEnvelope(
        domain_profile=profile.descriptor(),
        mode=mode,
        layer_values=normalized_values,
        result=result,
        audit=audit,
    )
    return envelope.model_dump()
