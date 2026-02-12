from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_detection_response_contract_shape(app) -> None:
    result = await app._tool_manager.call_tool(
        "mantic_detect",
        {
            "profile_name": "signal_core",
            "layer_values": [0.6, 0.6, 0.6, 0.6],
            "mode": "friction",
        },
    )
    payload = result.structured_content

    assert set(payload.keys()) == {
        "status",
        "contract_version",
        "domain_profile",
        "mode",
        "layer_values",
        "result",
        "audit",
    }

    assert set(payload["audit"].keys()) == {
        "overrides_applied",
        "clamped_fields",
        "rejected_fields",
        "calibration",
    }

    assert payload["status"] == "ok"
    assert payload["contract_version"] == "1.0.0"
