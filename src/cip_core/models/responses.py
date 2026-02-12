"""Response contracts used by the core MCP and SDK."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class AuditSummary(BaseModel):
    """Normalized audit envelope for strict output contracts."""

    model_config = ConfigDict(extra="forbid")

    overrides_applied: dict[str, Any] = Field(default_factory=dict)
    clamped_fields: list[str] = Field(default_factory=list)
    rejected_fields: list[str] = Field(default_factory=list)
    calibration: dict[str, Any] = Field(default_factory=dict)


class DetectionEnvelope(BaseModel):
    """Stable detection response shape for downstream consumers."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok"] = "ok"
    contract_version: str = "1.0.0"
    domain_profile: dict[str, Any]
    mode: Literal["friction", "emergence"]
    layer_values: list[float]
    result: dict[str, Any]
    audit: AuditSummary
