from __future__ import annotations

import os
from jinx.llm_primer import build_header_and_tag
from .gemini_caller import call_gemini, call_gemini_validated, call_gemini_stream_first_block
from jinx.log_paths import LLM_REQUESTS_DIR_GENERAL
from jinx.logger.llm_requests import write_llm_request_dump, write_llm_response_append
from jinx.micro.memory.storage import write_token_hint
from jinx.retry import detonate_payload
from .prompt_compose import compose_dynamic_prompt
from .macro_registry import MacroContext, expand_dynamic_macros
from .macro_providers import register_builtin_macros
from .macro_plugins import load_macro_plugins
from jinx.micro.conversation.cont import load_last_anchors
from jinx.micro.runtime.api import list_programs
import platform
import sys
import datetime as _dt
from .prompt_filters import sanitize_prompt_for_external_api
from jinx.micro.text.heuristics import is_code_like as _is_code_like
from jinx.micro.rt.timing import timing_section


async def code_primer(prompt_override: str | None = None) -> tuple[str, str]:
    """Build instruction header and return it with a code tag identifier.

    Returns (header_plus_prompt, code_tag_id).
    """
    return await build_header_and_tag(prompt_override)


async def _prepare_request(txt: str, *, prompt_override: str | None = None) -> tuple[str, str, str, str, str]:
    """Compose instructions and return (jx, tag, model, sx, stxt)."""
    jx, tag = await code_primer(prompt_override)
    
    # Get the model from environment or use default
    model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    # Sanitize the input text if needed
    stxt = sanitize_prompt_for_external_api(txt)
    
    # Prepare the system prompt (sx) - using instructions as system prompt
    sx = jx
    
    return jx, tag, model, sx, stxt


async def spark_gemini(txt: str, *, prompt_override: str | None = None) -> tuple[str, str]:
    """Call Gemini API and return output text with the code tag.

    Returns (output_text, code_tag_id).
    """
    jx, tag, model, sx, stxt = await _prepare_request(txt, prompt_override=prompt_override)

    async def gemini_task() -> tuple[str, str]:
        req_path: str = ""
        import asyncio as _asyncio
        # Overlap request dump with LLM call
        dump_task = _asyncio.create_task(write_llm_request_dump(
            target_dir=LLM_REQUESTS_DIR_GENERAL,
            kind="GENERAL",
            instructions=sx,
            input_text=stxt,
            model=model,
        ))
        # Preferred: validated multi-sample path
        try:
            async with timing_section("llm.call"):
                out = await call_gemini_validated(sx, model, stxt, code_id=tag)
        except Exception:
            # Fallback to legacy single-sample on error
            async with timing_section("llm.call_legacy"):
                out = await call_gemini(sx, model, stxt)
        # Get dump path (await, then append in background)
        try:
            req_path = await dump_task
        except Exception:
            req_path = ""
        try:
            _asyncio.create_task(write_llm_response_append(req_path, "GENERAL", out))
        except Exception:
            pass
        return (out, tag)

    # Avoid duplicate outbound API calls on post-call exceptions by disabling retries here.
    # Lower-level resiliency is provided by caching/coalescing/multi-path logic.
    return await detonate_payload(gemini_task, retries=1)


async def spark_gemini_streaming(txt: str, *, prompt_override: str | None = None, on_first_block=None) -> tuple[str, str]:
    """Streaming LLM call with early execution on first complete <python_{tag}> block.

    Returns (full_output_text, code_tag_id).
    """
    jx, tag, model, sx, stxt = await _prepare_request(txt, prompt_override=prompt_override)

    async def gemini_task() -> tuple[str, str]:
        req_path: str = ""
        import asyncio as _asyncio
        dump_task = _asyncio.create_task(write_llm_request_dump(
            target_dir=LLM_REQUESTS_DIR_GENERAL,
            kind="GENERAL",
            instructions=sx,
            input_text=stxt,
            model=model,
        ))
        try:
            async with timing_section("llm.stream"):
                out = await call_gemini_stream_first_block(sx, model, stxt, code_id=tag, on_first_block=on_first_block)
        except Exception:
            async with timing_section("llm.call_fallback"):
                out = await call_gemini_validated(sx, model, stxt, code_id=tag)
        try:
            req_path = await dump_task
        except Exception:
            req_path = ""
        try:
            _asyncio.create_task(write_llm_response_append(req_path, "GENERAL", out))
        except Exception:
            pass
        return (out, tag)

    return await detonate_payload(gemini_task, retries=1)


# Backward compatibility aliases
spark_openai = spark_gemini
spark_openai_streaming = spark_gemini_streaming


__all__ = [
    "code_primer",
    "spark_gemini",
    "spark_gemini_streaming",
    "spark_openai",  # Backward compatibility
    "spark_openai_streaming",  # Backward compatibility
]
