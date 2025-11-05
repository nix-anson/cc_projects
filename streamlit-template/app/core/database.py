"""Database connection and session management."""

from contextlib import contextmanager
from typing import Generator

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# Base class for models
Base = declarative_base()


@st.cache_resource
def get_engine() -> Engine:
    """
    Create and cache database engine.

    Returns:
        SQLAlchemy engine instance
    """
    database_url = st.secrets.get("database", {}).get(
        "url", "sqlite:///./app.db"
    )

    return create_engine(
        database_url,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=3600,  # Recycle connections after 1 hour
        echo=False,  # Set to True for SQL logging
    )


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.

    Yields:
        SQLAlchemy session instance

    Example:
        with get_session() as session:
            users = session.query(User).all()
    """
    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    """Initialize database (create tables)."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
