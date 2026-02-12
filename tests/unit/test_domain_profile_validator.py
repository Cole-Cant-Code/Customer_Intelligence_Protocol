from __future__ import annotations

from cip_core.domain_profiles.validator import validate_profile_payload


def _valid_payload() -> dict:
    return {
        "domain_name": "test_signal_domain",
        "version": "1.0.0",
        "display_name": "Test Signal Domain",
        "description": "Test profile",
        "layer_names": ["a_layer", "b_layer", "c_layer", "d_layer"],
        "weights": [0.25, 0.25, 0.25, 0.25],
        "hierarchy": {
            "a_layer": "Micro",
            "b_layer": "Meso",
            "c_layer": "Macro",
            "d_layer": "Meta",
        },
        "thresholds": {"detection": 0.4},
        "temporal_allowlist": ["linear", "memory"],
        "interaction_rules": {
            "default_mode": "dynamic",
            "default_override_mode": "scale",
            "min_value": 0.1,
            "max_value": 2.0,
        },
        "guardrails": {
            "disclaimers": ["Directional, not deterministic"],
            "prohibited_actions": ["No diagnoses"],
            "escalation_triggers": ["Sustained divergence"],
        },
    }


def test_valid_profile_payload_passes() -> None:
    ok, errors, profile = validate_profile_payload(_valid_payload())
    assert ok is True
    assert errors == []
    assert profile is not None
    assert profile.domain_name == "test_signal_domain"


def test_reserved_domain_name_fails() -> None:
    payload = _valid_payload()
    payload["domain_name"] = "finance"

    ok, errors, profile = validate_profile_payload(payload)
    assert ok is False
    assert profile is None
    assert any("collides" in error for error in errors)


def test_weights_must_sum_to_one() -> None:
    payload = _valid_payload()
    payload["weights"] = [0.4, 0.2, 0.2, 0.1]

    ok, errors, profile = validate_profile_payload(payload)
    assert ok is False
    assert profile is None
    assert any("sum to 1.0" in error for error in errors)


def test_temporal_allowlist_rejects_unknown_kernel() -> None:
    payload = _valid_payload()
    payload["temporal_allowlist"] = ["linear", "warp_drive"]

    ok, errors, profile = validate_profile_payload(payload)
    assert ok is False
    assert profile is None
    assert any("unsupported kernel" in error for error in errors)
