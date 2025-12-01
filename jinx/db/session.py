from __future__ import annotations

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL is configurable via env var; default to sqlite file in project root
DATABASE_URL = os.getenv("JINX_DATABASE_URL", "sqlite:///./jinx.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()


def get_session():
    """Yield a new DB session. Caller is responsible for closing."""
    return SessionLocal()


def init_db():
    """Create database tables if they do not exist."""
    from . import models  # noqa: F401 (ensure models are imported so metadata is registered)

    Base.metadata.create_all(bind=engine)
