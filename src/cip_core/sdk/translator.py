"""Translator protocol for downstream domain MCP adapters."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field


class TranslationResult(BaseModel):
    """Normalized translator output expected by core detection wrappers."""

    model_config = ConfigDict(extra="forbid")

    layer_values: list[float]
    details: dict[str, Any] = Field(default_factory=dict)


class DomainTranslator(Protocol):
    """Protocol that downstream domains implement to map raw context -> layer values."""

    def translate(self, raw_context: Mapping[str, Any]) -> TranslationResult:
        """Translate raw context into ordered layer values."""
        raise NotImplementedError
