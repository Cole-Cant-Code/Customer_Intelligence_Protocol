"""Server entry point for `python -m cip_core.server.main`."""

from __future__ import annotations

import logging
from ipaddress import ip_address

from cip_core.config.settings import get_settings
from cip_core.server.app import create_app


def _is_loopback_host(host: str) -> bool:
    if host == "localhost":
        return True
    try:
        return ip_address(host).is_loopback
    except ValueError:
        return False



def run() -> None:
    """Run the MCP server with secure default bind behavior."""
    settings = get_settings()
    logging.basicConfig(level=getattr(logging, settings.cip_log_level.upper(), logging.INFO))

    if not settings.cip_allow_insecure_bind and not _is_loopback_host(settings.cip_host):
        raise RuntimeError(
            "Refusing to bind server to non-loopback host without auth boundary. "
            "Set CIP_ALLOW_INSECURE_BIND=true to override (unsafe)."
        )

    server = create_app()
    server.run(
        transport="streamable-http",
        host=settings.cip_host,
        port=settings.cip_port,
    )


if __name__ == "__main__":
    run()
