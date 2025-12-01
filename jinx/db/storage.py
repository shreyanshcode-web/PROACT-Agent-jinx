from __future__ import annotations

import os
import time
from typing import Optional

from .session import get_session
from .models_memory import MemoryEntry, HistorySnapshot


def ensure_nl(s: str) -> str:
    return s + ("\n" if s and not s.endswith("\n") else "")


def memory_dir() -> str:
    return os.getenv("JINX_MEMORY_DIR", os.path.join(".jinx", "memory"))


def read_evergreen() -> str:
    """Return the evergreen memory content stored in DB, or empty string."""
    session = get_session()
    try:
        row = session.query(MemoryEntry).filter(MemoryEntry.key == "evergreen").first()
        return row.content if row and row.content is not None else ""
    finally:
        session.close()


def read_compact() -> str:
    session = get_session()
    try:
        row = session.query(MemoryEntry).filter(MemoryEntry.key == "compact").first()
        return row.content if row and row.content is not None else ""
    finally:
        session.close()


def get_memory_mtimes() -> tuple[int, int]:
    """Return (compact_mtime_ms, evergreen_mtime_ms) based on DB updated_at timestamps."""
    session = get_session()
    try:
        c = 0
        e = 0
        r = session.query(MemoryEntry).filter(MemoryEntry.key == "compact").first()
        if r and r.updated_at:
            c = int(r.updated_at.timestamp() * 1000)
        r = session.query(MemoryEntry).filter(MemoryEntry.key == "evergreen").first()
        if r and r.updated_at:
            e = int(r.updated_at.timestamp() * 1000)
        return (c, e)
    finally:
        session.close()


def read_channel(kind: str) -> str:
    key = f"channel:{(kind or '').strip().lower()}"
    session = get_session()
    try:
        row = session.query(MemoryEntry).filter(MemoryEntry.key == key).first()
        return row.content if row and row.content is not None else ""
    finally:
        session.close()


def read_topic(name: str) -> str:
    if not (name or "").strip():
        return ""
    key = f"topic:{name}"
    session = get_session()
    try:
        row = session.query(MemoryEntry).filter(MemoryEntry.key == key).first()
        return row.content if row and row.content is not None else ""
    finally:
        session.close()


def write_open_buffers(buffers: list[dict]) -> None:
    import json
    payload = json.dumps(buffers or [])
    session = get_session()
    try:
        row = session.query(MemoryEntry).filter(MemoryEntry.key == "open_buffers").first()
        if row is None:
            row = MemoryEntry(key="open_buffers", content=payload)
            session.add(row)
        else:
            row.content = payload
        session.commit()
    finally:
        session.close()


def open_buffers_path() -> str:
    return "db://open_buffers"


def write_token_hint(tokens: int) -> None:
    session = get_session()
    try:
        row = session.query(MemoryEntry).filter(MemoryEntry.key == "token_hint").first()
        if row is None:
            row = MemoryEntry(key="token_hint", content=str(int(tokens)))
            session.add(row)
        else:
            row.content = str(int(tokens))
        session.commit()
    finally:
        session.close()


def read_token_hint() -> int:
    session = get_session()
    try:
        row = session.query(MemoryEntry).filter(MemoryEntry.key == "token_hint").first()
        if row and row.content:
            try:
                return int(row.content)
            except Exception:
                return 0
        return 0
    finally:
        session.close()


def _parse_channels(durable_text: str) -> dict[str, list[str]]:
    buckets = {"paths": [], "symbols": [], "prefs": [], "decisions": []}
    for raw in (durable_text or "").splitlines():
        line = (raw or "").strip()
        if not line:
            continue
        low = line.lower()
        if low.startswith("path: "):
            buckets["paths"].append(line)
        elif low.startswith("symbol: "):
            buckets["symbols"].append(line)
        elif low.startswith("pref: "):
            buckets["prefs"].append(line)
        elif low.startswith("decision: "):
            buckets["decisions"].append(line)
    return buckets


def write_state(compact: str, durable: Optional[str]) -> None:
    """Persist compact and durable memory into DB and append a history snapshot."""
    session = get_session()
    try:
        # compact
        r = session.query(MemoryEntry).filter(MemoryEntry.key == "compact").first()
        if r is None:
            r = MemoryEntry(key="compact", content=ensure_nl(compact))
            session.add(r)
        else:
            r.content = ensure_nl(compact)

        # durable / evergreen
        if durable is not None:
            er = session.query(MemoryEntry).filter(MemoryEntry.key == "evergreen").first()
            if er is None:
                er = MemoryEntry(key="evergreen", content=ensure_nl(durable))
                session.add(er)
            else:
                er.content = ensure_nl(durable)
            # derive channels
            buckets = _parse_channels(durable)
            for k, v in buckets.items():
                key = f"channel:{k}"
                row = session.query(MemoryEntry).filter(MemoryEntry.key == key).first()
                content = ensure_nl("\n".join(v))
                if row is None:
                    session.add(MemoryEntry(key=key, content=content))
                else:
                    row.content = content

        # history snapshot
        ts = int(time.time() * 1000)
        snap = HistorySnapshot(ts_ms=ts, compact=ensure_nl(compact), evergreen=ensure_nl(durable or ""))
        session.add(snap)

        session.commit()
    finally:
        session.close()
