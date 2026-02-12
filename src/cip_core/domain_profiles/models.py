"""Canonical domain profile models."""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from cip_core.domain_profiles.constants import (
    ALLOWED_HIERARCHY_LEVELS,
    ALLOWED_KERNEL_TYPES,
    RESERVED_DOMAIN_NAMES,
)


class InteractionRules(BaseModel):
    """Policy for interaction-coefficient control."""

    model_config = ConfigDict(extra="forbid")

    default_mode: Literal["dynamic", "base"] = "dynamic"
    default_override_mode: Literal["scale", "replace"] = "scale"
    min_value: float = 0.1
    max_value: float = 2.0

    @model_validator(mode="after")
    def validate_bounds(self) -> InteractionRules:
        if self.min_value < 0.1:
            raise ValueError("interaction_rules.min_value must be >= 0.1")
        if self.max_value > 2.0:
            raise ValueError("interaction_rules.max_value must be <= 2.0")
        if self.min_value >= self.max_value:
            raise ValueError("interaction_rules.min_value must be < max_value")
        return self


class Guardrails(BaseModel):
    """Policy guardrails for downstream MCP interpretive layers."""

    model_config = ConfigDict(extra="forbid")

    disclaimers: list[str] = Field(default_factory=list)
    prohibited_actions: list[str] = Field(default_factory=list)
    escalation_triggers: list[str] = Field(default_factory=list)

    @field_validator("disclaimers", "prohibited_actions", "escalation_triggers")
    @classmethod
    def validate_string_list(cls, value: list[str]) -> list[str]:
        for item in value:
            if not isinstance(item, str) or not item.strip():
                raise ValueError("guardrail entries must be non-empty strings")
        return value


class DomainProfile(BaseModel):
    """Canonical profile contract used by core MCP and downstream domain MCPs."""

    model_config = ConfigDict(extra="forbid")

    domain_name: str
    version: str = "1.0.0"
    display_name: str = ""
    description: str = ""

    layer_names: list[str]
    weights: list[float]
    hierarchy: dict[str, str]

    thresholds: dict[str, float] = Field(default_factory=lambda: {"detection": 0.4})
    temporal_allowlist: list[str] = Field(default_factory=lambda: ["linear", "memory"])
    interaction_rules: InteractionRules = Field(default_factory=InteractionRules)
    guardrails: Guardrails = Field(default_factory=Guardrails)

    @field_validator("domain_name")
    @classmethod
    def validate_domain_name(cls, value: str) -> str:
        if value.lower() in RESERVED_DOMAIN_NAMES:
            raise ValueError(
                f"domain_name '{value}' collides with reserved Mantic domains: "
                f"{sorted(RESERVED_DOMAIN_NAMES)}"
            )
        if not re.match(r"^[a-z][a-z0-9_-]{2,63}$", value):
            raise ValueError(
                "domain_name must match ^[a-z][a-z0-9_-]{2,63}$"
            )
        return value

    @field_validator("version")
    @classmethod
    def validate_version(cls, value: str) -> str:
        if not re.match(r"^\d+\.\d+\.\d+$", value):
            raise ValueError("version must be semantic format like '1.0.0'")
        return value

    @field_validator("layer_names")
    @classmethod
    def validate_layer_names(cls, value: list[str]) -> list[str]:
        if not 3 <= len(value) <= 6:
            raise ValueError("layer_names must contain between 3 and 6 entries")
        if len(set(value)) != len(value):
            raise ValueError("layer_names must be unique")
        for name in value:
            if not re.match(r"^[a-z][a-z0-9_]{1,63}$", name):
                raise ValueError(
                    "layer names must match ^[a-z][a-z0-9_]{1,63}$"
                )
        return value

    @field_validator("weights")
    @classmethod
    def validate_weights(cls, value: list[float]) -> list[float]:
        for weight in value:
            if weight < 0 or weight > 1:
                raise ValueError("weights must be within [0, 1]")
        return value

    @field_validator("hierarchy")
    @classmethod
    def validate_hierarchy_levels(cls, value: dict[str, str]) -> dict[str, str]:
        for _, level in value.items():
            if level not in ALLOWED_HIERARCHY_LEVELS:
                raise ValueError(
                    f"hierarchy values must be one of {sorted(ALLOWED_HIERARCHY_LEVELS)}"
                )
        return value

    @field_validator("thresholds")
    @classmethod
    def validate_threshold_values(cls, value: dict[str, float]) -> dict[str, float]:
        for key, threshold in value.items():
            if not isinstance(threshold, (int, float)):
                raise ValueError(f"threshold '{key}' must be numeric")
            if threshold <= 0 or threshold >= 1:
                raise ValueError(f"threshold '{key}' must be in (0, 1)")
        return value

    @field_validator("temporal_allowlist")
    @classmethod
    def validate_temporal_allowlist(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("temporal_allowlist must not be empty")
        for kernel in value:
            if kernel not in ALLOWED_KERNEL_TYPES:
                raise ValueError(
                    f"temporal_allowlist includes unsupported kernel '{kernel}'"
                )
        return value

    @model_validator(mode="after")
    def validate_cross_field_consistency(self) -> DomainProfile:
        if len(self.weights) != len(self.layer_names):
            raise ValueError("weights length must equal layer_names length")

        weight_sum = sum(self.weights)
        if not 0.999 <= weight_sum <= 1.001:
            raise ValueError(f"weights must sum to 1.0 (got {weight_sum:.6f})")

        if set(self.hierarchy.keys()) != set(self.layer_names):
            raise ValueError("hierarchy keys must match layer_names exactly")

        if "detection" not in self.thresholds:
            raise ValueError("thresholds must include 'detection'")

        return self

    @property
    def detection_threshold(self) -> float:
        """Primary detection threshold used by generic_detect."""
        return float(self.thresholds["detection"])

    def descriptor(self) -> dict[str, object]:
        """Public metadata exposed by MCP tools."""
        return {
            "domain_name": self.domain_name,
            "version": self.version,
            "display_name": self.display_name,
            "description": self.description,
            "layer_names": self.layer_names,
            "thresholds": self.thresholds,
            "temporal_allowlist": self.temporal_allowlist,
        }
