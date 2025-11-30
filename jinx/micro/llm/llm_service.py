from __future__ import annotations

import os
from typing import Any, Dict, Optional

# Provider‑specific low‑level functions
from .gemini_service import spark_gemini, spark_gemini_streaming
from .llm_cache import call_gemini_cached

# Default configuration (can be overridden via environment variables)
DEFAULT_MODEL = os.getenv("LLM_MODEL", "gemini-pro")
DEFAULT_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
DEFAULT_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))


async def call_llm(
    prompt: str,
    *,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    stream: bool = False,
    extra_kwargs: Optional[Dict[str, Any]] = None,
) -> str:
    """Unified LLM call with optional caching and configurable parameters.

    Parameters
    ----------
    prompt: str
        The user prompt or instructions.
    model: str, optional
        Model name; defaults to ``LLM_MODEL`` env var.
    temperature: float, optional
        Sampling temperature; defaults to ``LLM_TEMPERATURE``.
    max_tokens: int, optional
        Maximum output tokens; defaults to ``LLM_MAX_TOKENS``.
    stream: bool, default False
        If ``True`` use the streaming Gemini endpoint (no caching).
    extra_kwargs: dict, optional
        Additional provider‑specific arguments.

    Returns
    -------
    str
        Generated text (without the code‑tag wrapper).
    """
    # Resolve configuration
    model = model or DEFAULT_MODEL
    extra: Dict[str, Any] = extra_kwargs.copy() if extra_kwargs else {}
    extra["temperature"] = temperature if temperature is not None else DEFAULT_TEMPERATURE
    extra["max_tokens"] = max_tokens if max_tokens is not None else DEFAULT_MAX_TOKENS

    if stream:
        # Streaming path – currently not cached.
        out, _ = await spark_gemini_streaming(prompt, prompt_override=None, on_first_block=None)
        return out

    # Cached call – reuse existing Gemini cache logic.
    return await call_gemini_cached(instructions=prompt, model=model, input_text=prompt, extra_kwargs=extra)
