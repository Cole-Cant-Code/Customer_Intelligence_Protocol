from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from cip_core.sdk.translator import TranslationResult
from cip_core.sdk.wrappers import detect_from_translator, load_registry


class _EchoTranslator:
    def translate(self, raw_context: Mapping[str, Any]) -> TranslationResult:
        values = raw_context["layer_values"]
        return TranslationResult(layer_values=list(values), details={"source": "test"})


def test_detect_from_translator_runs_detection(profiles_dir) -> None:
    registry = load_registry(profiles_dir)
    translator = _EchoTranslator()

    result = detect_from_translator(
        registry=registry,
        profile_name="customer_signal_core",
        translator=translator,
        raw_context={"layer_values": [0.62, 0.71, 0.45, 0.58]},
        mode="friction",
    )

    assert result["status"] == "ok"
    assert result["mode"] == "friction"
    assert "m_score" in result["result"]


def test_detect_from_translator_passes_f_time(profiles_dir) -> None:
    registry = load_registry(profiles_dir)
    translator = _EchoTranslator()

    result = detect_from_translator(
        registry=registry,
        profile_name="customer_signal_core",
        translator=translator,
        raw_context={"layer_values": [0.62, 0.71, 0.45, 0.58]},
        mode="emergence",
        f_time=1.9,
    )

    assert result["result"]["overrides_applied"]["f_time"]["requested"] == 1.9
