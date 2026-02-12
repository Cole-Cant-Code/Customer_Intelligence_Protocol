"""FastMCP application factory for CIP Mantic Core."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from fastmcp import FastMCP

from cip_core import __version__
from cip_core.config.settings import get_settings
from cip_core.domain_profiles.registry import DomainProfileRegistry
from cip_core.domain_profiles.validator import validate_profile_yaml
from cip_core.mantic.runtime import run_detection

logger = logging.getLogger(__name__)



def _error_response(message: str, *, code: str = "validation_error") -> dict[str, Any]:
    return {
        "status": "error",
        "error": {
            "code": code,
            "message": message,
        },
    }



def create_app(
    *,
    profile_registry_override: DomainProfileRegistry | None = None,
    profiles_dir_override: str | Path | None = None,
) -> FastMCP:
    """Create and configure the Mantic-first MCP server."""
    settings = get_settings()

    raw_dir = Path(profiles_dir_override or settings.cip_profiles_dir)
    # Anchor relative paths to the project root (alongside pyproject.toml)
    if not raw_dir.is_absolute():
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        profile_dir = project_root / raw_dir
    else:
        profile_dir = raw_dir
    if profile_registry_override is not None:
        registry = profile_registry_override
    else:
        registry = DomainProfileRegistry.from_directory(profile_dir)

    logger.info("Loaded %d domain profiles from %s", len(registry), profile_dir)

    server = FastMCP(
        "CIP Mantic Core",
        instructions=(
            "Mantic-first core MCP server for cross-domain reasoning. "
            "Exposes deterministic Mantic detection tools plus domain profile "
            "contract validation and registry discovery."
        ),
    )

    def _run_mantic_detect(
        *,
        profile_name: str,
        layer_values: list[float],
        mode: str,
        f_time: float = 1.0,
        threshold_override: dict[str, float] | None = None,
        temporal_config: dict[str, Any] | None = None,
        interaction_mode: str = "dynamic",
        interaction_override: dict[str, float] | list[float] | None = None,
        interaction_override_mode: str = "scale",
    ) -> dict[str, Any]:
        try:
            profile = registry.get(profile_name)
            if mode not in {"friction", "emergence"}:
                return _error_response("mode must be 'friction' or 'emergence'")
            if interaction_mode not in {"dynamic", "base"}:
                return _error_response(
                    "interaction_mode must be 'dynamic' or 'base'"
                )
            if interaction_override_mode not in {"scale", "replace"}:
                return _error_response(
                    "interaction_override_mode must be 'scale' or 'replace'"
                )

            envelope = run_detection(
                profile=profile,
                layer_values=layer_values,
                mode=mode,
                f_time=f_time,
                threshold_override=threshold_override,
                temporal_config=temporal_config,
                interaction_mode=interaction_mode,
                interaction_override=interaction_override,
                interaction_override_mode=interaction_override_mode,
            )
            return envelope
        except KeyError as exc:
            return _error_response(str(exc), code="unknown_profile")
        except Exception as exc:
            logger.exception("mantic_detect failed")
            return _error_response(str(exc), code="runtime_error")

    @server.tool
    def health_check() -> dict[str, Any]:
        """Check server readiness and profile load state."""
        return {
            "status": "ok",
            "server": "CIP Mantic Core",
            "version": __version__,
            "profiles_loaded": len(registry),
        }

    @server.tool
    def list_domain_profiles() -> dict[str, Any]:
        """List registered domain profiles available for detection."""
        return {
            "status": "ok",
            "count": len(registry),
            "profiles": registry.list(),
        }

    @server.tool
    def validate_domain_profile(profile_yaml: str) -> dict[str, Any]:
        """Validate a domain profile YAML document against canonical schema."""
        is_valid, errors, profile = validate_profile_yaml(profile_yaml)
        response: dict[str, Any] = {
            "status": "ok",
            "valid": is_valid,
            "errors": errors,
        }
        if profile is not None:
            response["profile"] = profile.model_dump()
            response["descriptor"] = profile.descriptor()
        return response

    @server.tool
    def mantic_detect(
        profile_name: str,
        layer_values: list[float],
        mode: str = "friction",
        f_time: float = 1.0,
        threshold_override: dict[str, float] | None = None,
        temporal_config: dict[str, Any] | None = None,
        interaction_mode: str = "dynamic",
        interaction_override: dict[str, float] | list[float] | None = None,
        interaction_override_mode: str = "scale",
    ) -> dict[str, Any]:
        """Run profile-based Mantic detection in friction or emergence mode."""
        return _run_mantic_detect(
            profile_name=profile_name,
            layer_values=layer_values,
            mode=mode,
            f_time=f_time,
            threshold_override=threshold_override,
            temporal_config=temporal_config,
            interaction_mode=interaction_mode,
            interaction_override=interaction_override,
            interaction_override_mode=interaction_override_mode,
        )

    @server.tool
    def mantic_detect_friction(
        profile_name: str,
        layer_values: list[float],
        f_time: float = 1.0,
        threshold_override: dict[str, float] | None = None,
        temporal_config: dict[str, Any] | None = None,
        interaction_mode: str = "dynamic",
        interaction_override: dict[str, float] | list[float] | None = None,
        interaction_override_mode: str = "scale",
    ) -> dict[str, Any]:
        """Run profile-based Mantic friction detection."""
        return _run_mantic_detect(
            profile_name=profile_name,
            layer_values=layer_values,
            mode="friction",
            f_time=f_time,
            threshold_override=threshold_override,
            temporal_config=temporal_config,
            interaction_mode=interaction_mode,
            interaction_override=interaction_override,
            interaction_override_mode=interaction_override_mode,
        )

    @server.tool
    def mantic_detect_emergence(
        profile_name: str,
        layer_values: list[float],
        f_time: float = 1.0,
        threshold_override: dict[str, float] | None = None,
        temporal_config: dict[str, Any] | None = None,
        interaction_mode: str = "dynamic",
        interaction_override: dict[str, float] | list[float] | None = None,
        interaction_override_mode: str = "scale",
    ) -> dict[str, Any]:
        """Run profile-based Mantic emergence detection."""
        return _run_mantic_detect(
            profile_name=profile_name,
            layer_values=layer_values,
            mode="emergence",
            f_time=f_time,
            threshold_override=threshold_override,
            temporal_config=temporal_config,
            interaction_mode=interaction_mode,
            interaction_override=interaction_override,
            interaction_override_mode=interaction_override_mode,
        )

    return server



def __getattr__(name: str):
    # FastMCP config references `app.py:mcp`; lazily create it for import-time discovery.
    if name == "mcp":
        global mcp
        mcp = create_app()
        return mcp
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
