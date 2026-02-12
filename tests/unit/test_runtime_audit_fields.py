from __future__ import annotations

from cip_core.mantic.runtime import _extract_clamped_fields, _extract_rejected_fields


def test_extract_clamped_fields_collects_expected_paths() -> None:
    overrides = {
        "threshold_overrides": {"clamped": True},
        "temporal_config": {
            "clamped": {
                "alpha": {"requested": 0.9, "used": 0.5},
                "n": {"requested": 10, "used": 2.0},
            }
        },
        "f_time": {"clamped": True},
        "interaction": {
            "clamped": {
                "risk": {"requested": 3.0, "used": 2.0},
                "macro": {"requested": 0.01, "used": 0.1},
            }
        },
    }

    assert _extract_clamped_fields(overrides) == [
        "f_time",
        "interaction.macro",
        "interaction.risk",
        "temporal_config.alpha",
        "temporal_config.n",
        "threshold_overrides",
    ]


def test_extract_rejected_fields_collects_expected_paths() -> None:
    overrides = {
        "temporal_config": {
            "rejected": {
                "kernel_type": {"requested": "warp_drive"},
                "t": {"requested": "NaN"},
            }
        },
        "interaction": {
            "rejected": {
                "unknown_layer": {"requested": 1.2},
            }
        },
        "threshold_overrides": {
            "ignored_keys": ["alignment", "confidence"],
        },
    }

    assert _extract_rejected_fields(overrides) == [
        "interaction.unknown_layer",
        "temporal_config.kernel_type",
        "temporal_config.t",
        "threshold_override.alignment",
        "threshold_override.confidence",
    ]
