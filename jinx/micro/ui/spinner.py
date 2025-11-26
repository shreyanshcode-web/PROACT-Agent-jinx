from __future__ import annotations

"""Spinner micro-module.

Renders a non-blocking terminal spinner while background tasks are running.
The spinner terminates when the provided event is set.
"""

import asyncio
import time
import sys
import random
import importlib

from jinx.bootstrap import ensure_optional
from jinx.spinner.phrases import PHRASES as phrases
from jinx.spinner import ascii_mode as _ascii_mode, can_render as _can_render
from jinx.spinner import get_spinner_frames, get_hearts
import jinx.state as state

# Lazy import with auto-install of prompt_toolkit
ensure_optional(["prompt_toolkit"])  # installs if missing
print_formatted_text = importlib.import_module("prompt_toolkit").print_formatted_text  # type: ignore[assignment]
FormattedText = importlib.import_module("prompt_toolkit.formatted_text").FormattedText  # type: ignore[assignment]


async def sigil_spin(evt: asyncio.Event) -> None:
    """Minimal, pretty spinner that shows pulse and spins until evt is set.

    Parameters
    ----------
    evt : asyncio.Event
        Event signaling spinner shutdown.
    """
    enc = getattr(sys.stdout, "encoding", None) or "utf-8"
    fx = print_formatted_text
    ft = FormattedText
    t0 = time.perf_counter()
    ascii_mode = _ascii_mode()
    heart_a, heart_b = get_hearts(ascii_mode, can=lambda s: _can_render(s, enc))
    # Thin circular spinner frames (Unicode) with ASCII fallback
    spin_frames = get_spinner_frames(ascii_mode, can=lambda s: _can_render(s, enc))
    
    # Static message
    phrase = "Thinking..."
    
    while not evt.is_set():
        dt = time.perf_counter() - t0
        pulse = state.pulse
        clr = "ansibrightgreen"

        # Loading dots cadence (0..3 dots cycling)
        n = int(dt * 2) % 4
        dd = "." * n
        
        # Pulsating heart (toggle ~1.5 Hz)
        beat = int(dt * 1.5) % 2
        heart = heart_a if beat == 0 else heart_b
        style = clr if beat == 0 else f"{clr} bold"

        # ASCII spinner (~12 FPS)
        sidx = int(dt * 12) % len(spin_frames)
        spin = spin_frames[sidx]

        # Simple static output
        fx(ft([(style, f"{heart} {spin} {phrase} {dd} ({dt:.1f}s)")]), end="\r", flush=True)
        await asyncio.sleep(0.05)

    fx(ft([("", " " * 80)]), end="\r", flush=True)


__all__ = [
    "sigil_spin",
]
