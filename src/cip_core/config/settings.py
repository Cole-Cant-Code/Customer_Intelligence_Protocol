"""Application settings loaded from environment variables."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """CIP Mantic Core server settings."""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    cip_host: str = "127.0.0.1"
    cip_port: int = 8010
    cip_log_level: str = "info"
    cip_allow_insecure_bind: bool = False

    cip_profiles_dir: str = "profiles"



def get_settings() -> Settings:
    """Return hydrated settings instance."""
    return Settings()
