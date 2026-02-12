from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_core_tool_surface_registered(app) -> None:
    tools = await app.get_tools()
    names = sorted(tools.keys())
    assert names == [
        "health_check",
        "list_domain_profiles",
        "mantic_detect",
        "mantic_detect_emergence",
        "mantic_detect_friction",
        "validate_domain_profile",
    ]


@pytest.mark.asyncio
async def test_list_domain_profiles_tool(app) -> None:
    result = await app._tool_manager.call_tool("list_domain_profiles", {})
    payload = result.structured_content

    assert payload["status"] == "ok"
    assert payload["count"] >= 1
    assert payload["profiles"][0]["domain_name"] == "customer_signal_core"


@pytest.mark.asyncio
async def test_validate_domain_profile_tool(app, profiles_dir) -> None:
    valid_yaml = (profiles_dir / "customer_signal_core.v1.yaml").read_text(encoding="utf-8")

    valid = await app._tool_manager.call_tool(
        "validate_domain_profile",
        {"profile_yaml": valid_yaml},
    )
    assert valid.structured_content["valid"] is True

    invalid = await app._tool_manager.call_tool(
        "validate_domain_profile",
        {"profile_yaml": "domain_name: finance\nversion: bad"},
    )
    assert invalid.structured_content["valid"] is False
    assert invalid.structured_content["errors"]


@pytest.mark.asyncio
async def test_end_to_end_mantic_detection_tools(app) -> None:
    args = {
        "profile_name": "customer_signal_core",
        "layer_values": [0.62, 0.71, 0.45, 0.58],
    }

    friction = await app._tool_manager.call_tool("mantic_detect_friction", args)
    f_payload = friction.structured_content
    assert f_payload["status"] == "ok"
    assert f_payload["mode"] == "friction"
    assert "m_score" in f_payload["result"]

    emergence = await app._tool_manager.call_tool("mantic_detect_emergence", args)
    e_payload = emergence.structured_content
    assert e_payload["status"] == "ok"
    assert e_payload["mode"] == "emergence"
    assert "m_score" in e_payload["result"]


@pytest.mark.asyncio
async def test_invalid_interaction_modes_return_validation_error(app) -> None:
    result = await app._tool_manager.call_tool(
        "mantic_detect",
        {
            "profile_name": "customer_signal_core",
            "layer_values": [0.62, 0.71, 0.45, 0.58],
            "mode": "friction",
            "interaction_mode": "invalid",
        },
    )
    payload = result.structured_content
    assert payload["status"] == "error"
    assert payload["error"]["code"] == "validation_error"
