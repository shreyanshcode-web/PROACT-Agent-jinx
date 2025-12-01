from __future__ import annotations

from sqlalchemy import Column, Integer, String, DateTime, func
from .session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, index=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def as_dict(self) -> dict:
        return {"id": self.id, "username": self.username, "created_at": self.created_at}
