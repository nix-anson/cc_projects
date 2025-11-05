"""Application configuration using Pydantic."""

from typing import Optional

import streamlit as st
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "Streamlit App"
    debug: bool = False

    # Database
    database_url: str = Field(
        default="sqlite:///./app.db",
        description="Database connection URL"
    )

    # API
    api_base_url: Optional[str] = None
    api_key: Optional[str] = None
    api_timeout: float = 10.0

    # Authentication
    session_timeout_minutes: int = 30

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False


@st.cache_resource
def get_settings() -> Settings:
    """
    Get cached application settings.

    Returns:
        Settings instance
    """
    # Try to load from Streamlit secrets first
    try:
        database_url = st.secrets.get("database", {}).get("url")
        api_base_url = st.secrets.get("api", {}).get("base_url")
        api_key = st.secrets.get("api", {}).get("key")

        return Settings(
            database_url=database_url or "sqlite:///./app.db",
            api_base_url=api_base_url,
            api_key=api_key,
        )
    except Exception:
        # Fall back to environment variables
        return Settings()
