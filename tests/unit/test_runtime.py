from __future__ import annotations

import pytest

from cip_core.domain_profiles.loader import load_profile_file
from cip_core.mantic import runtime
from cip_core.mantic.runtime import run_detection


def _profile(profiles_dir):
    return load_profile_file(profiles_dir / "customer_signal_core.v1.yaml")


def test_run_detection_returns_contract_envelope(profiles_dir) -> None:
    profile = _profile(profiles_dir)
    result = run_detection(
        profile=profile,
        layer_values=[0.6, 0.7, 0.5, 0.4],
        mode="friction",
    )

    assert result["status"] == "ok"
    assert result["contract_version"] == "1.0.0"
    assert result["mode"] == "friction"
    assert "result" in result
    assert "audit" in result
    assert "overrides_applied" in result["audit"]


def test_temporal_allowlist_is_enforced(profiles_dir) -> None:
    profile = _profile(profiles_dir)
    with pytest.raises(ValueError, match="not allowed"):
        run_detection(
            profile=profile,
            layer_values=[0.6, 0.7, 0.5, 0.4],
            mode="friction",
            temporal_config={"kernel_type": "power_law", "t": 1},
        )


def test_unknown_threshold_key_is_captured_in_audit(profiles_dir) -> None:
    profile = _profile(profiles_dir)
    result = run_detection(
        profile=profile,
        layer_values=[0.6, 0.7, 0.5, 0.4],
        mode="emergence",
        threshold_override={"alignment": 0.5},
    )

    assert "threshold_override.alignment" in result["audit"]["rejected_fields"]


def test_layer_values_are_clamped_to_unit_interval(profiles_dir) -> None:
    profile = _profile(profiles_dir)
    result = run_detection(
        profile=profile,
        layer_values=[1.2, -0.2, 0.5, 0.4],
        mode="friction",
    )

    assert result["layer_values"] == [1.0, 0.0, 0.5, 0.4]


def test_run_detection_supports_direct_f_time(profiles_dir) -> None:
    profile = _profile(profiles_dir)
    result = run_detection(
        profile=profile,
        layer_values=[0.6, 0.7, 0.5, 0.4],
        mode="friction",
        f_time=2.2,
    )

    assert result["result"]["overrides_applied"]["f_time"]["requested"] == 2.2


def test_run_detection_wraps_mantic_import_failure(profiles_dir, monkeypatch) -> None:
    profile = _profile(profiles_dir)

    real_import = __import__

    def _broken_import(name, *args, **kwargs):
        if name == "mantic_thinking.tools.generic_detect":
            raise ImportError("missing")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", _broken_import)

    with pytest.raises(RuntimeError, match="mantic-thinking is not installed"):
        runtime.run_detection(
            profile=profile,
            layer_values=[0.6, 0.7, 0.5, 0.4],
            mode="friction",
        )


def test_run_detection_propagates_detect_exceptions(profiles_dir, monkeypatch) -> None:
    profile = _profile(profiles_dir)

    def _boom(**_kwargs):
        raise RuntimeError("detect exploded")

    monkeypatch.setattr("mantic_thinking.tools.generic_detect.detect", _boom)

    with pytest.raises(RuntimeError, match="detect exploded"):
        runtime.run_detection(
            profile=profile,
            layer_values=[0.6, 0.7, 0.5, 0.4],
            mode="friction",
        )
