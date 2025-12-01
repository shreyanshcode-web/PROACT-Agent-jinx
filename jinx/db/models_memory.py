from __future__ import annotations

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .session import Base


class MemoryEntry(Base):
    __tablename__ = "memory_entries"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(128), unique=True, index=True, nullable=False)
    content = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class HistorySnapshot(Base):
    __tablename__ = "memory_history"

    id = Column(Integer, primary_key=True, index=True)
    ts_ms = Column(Integer, nullable=False, index=True)
    compact = Column(Text, nullable=True)
    evergreen = Column(Text, nullable=True)
