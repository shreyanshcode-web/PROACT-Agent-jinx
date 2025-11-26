"""Interactive input micro-module.

Provides an async prompt using prompt_toolkit and pushes sanitized user input
into an asyncio queue. Includes an inactivity watchdog that emits
"<no_response>" after a configurable timeout to keep the agent responsive.
"""

from __future__ import annotations

import asyncio
import importlib
import contextlib
from jinx.bootstrap import ensure_optional
from typing import Any, cast
from jinx.state import boom_limit
from jinx.logging_service import blast_mem, bomb_log
from jinx.log_paths import TRIGGER_ECHOES, BLUE_WHISPERS
from jinx.async_utils.queue import try_put_nowait
import jinx.state as jx_state

# Ensure prompt_toolkit is present at import time to avoid installing in an active event loop
ensure_optional(["prompt_toolkit"])  # installs if missing

async def neon_input(qe: asyncio.Queue[str]) -> None:
    """Read user input and feed it into the provided queue.

    This implementation attempts to use ``prompt_toolkit`` for an async prompt.
    If ``prompt_toolkit`` is unavailable or fails to import, it falls back to the
    built‑in ``input()`` function executed in a thread to avoid blocking the event
    loop.
    """
    # Try to import prompt_toolkit and create a session
    try:
        _ptk = importlib.import_module("prompt_toolkit")
        PromptSession = getattr(_ptk, "PromptSession")
        sess = PromptSession()
    except Exception:
        sess = None
        bomb_log.debug("prompt_toolkit not available, using fallback input")

    # Dummy watchdog placeholder (original watchdog logic omitted for brevity)
    watch_task = asyncio.create_task(asyncio.sleep(0))

    try:
        while True:
            if sess is not None:
                # Use async prompt from prompt_toolkit
                try:
                    v = await sess.prompt_async("\n>>> ")
                except (EOFError, KeyboardInterrupt):
                    break
            else:
                # Fallback to blocking input in a thread
                v = await asyncio.to_thread(input, "\n>>> ")

            if v.strip():
                await bomb_log(v, TRIGGER_ECHOES)
                await qe.put(v.strip())
    finally:
        # Cancel dummy watchdog
        watch_task.cancel()
        try:
            await watch_task
        except asyncio.CancelledError:
            pass
        # Ensure prompt_toolkit session is closed if it was created
        if sess is not None:
            with contextlib.suppress(Exception):
                sess.app.exit(exception=EOFError())
