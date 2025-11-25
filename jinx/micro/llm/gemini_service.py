from __future__ import annotations

import os
from jinx.openai_mod import build_header_and_tag
from .gemini_caller import call_gemini, call_gemini_validated, call_gemini_stream_first_block
from jinx.log_paths import OPENAI_REQUESTS_DIR_GENERAL
from jinx.logger.openai_requests import write_openai_request_dump, write_openai_response_append
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
    # Expand dynamic prompt macros in real time (vars/env/anchors/sys/runtime/exports + custom providers)
    try:
        jx = await compose_dynamic_prompt(jx, key=tag)
        # Auto-inject helpful embedding macros so the user doesn't need to type them
        try:
            auto_on = str(os.getenv("JINX_AUTOMACROS", "1")).lower() not in ("", "0", "false", "off", "no")
        except Exception:
            auto_on = True
        if auto_on and ("{{m:" not in jx or "{{m:emb:" not in jx or "{{m:mem:" not in jx):
            lines = []
            try:
                use_dlg = str(os.getenv("JINX_AUTOMACRO_DIALOGUE", "1")).lower() not in ("", "0", "false", "off", "no")
            except Exception:
                use_dlg = True
            try:
                use_proj = str(os.getenv("JINX_AUTOMACRO_PROJECT", "1")).lower() not in ("", "0", "false", "off", "no")
            except Exception:
                use_proj = True
            if use_dlg:
                lines.append("{{m:dialog}}")
            if use_proj:
                lines.append("{{m:project}}")
            if lines:
                jx = f"{' '.join(lines)}\n\n{jx}"
    except Exception as e:
        await bomb_log(f"Error expanding macros: {e}")
        # Continue with unexpanded prompt rather than failing
        pass

    # Get the model from environment or use default
    model = os.getenv("GEMINI_MODEL", "gemini-pro")
    
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
    
    # Call Gemini API
    try:
        response = await call_gemini(sx, model, stxt)
        return response, tag
    except Exception as e:
        await bomb_log(f"Gemini API call failed: {e}")
        raise


async def spark_gemini_streaming(
    txt: str, *, prompt_override: str | None = None, on_first_block=None
) -> tuple[str, str]:
    """Streaming LLM call with early execution on first complete <python_{tag}> block.

    Returns (full_output_text, code_tag_id).
    """
    jx, tag, model, sx, stxt = await _prepare_request(txt, prompt_override=prompt_override)
    
    # Call Gemini with streaming
    try:
        response = await call_gemini_stream_first_block(
            sx,
            model,
            stxt,
            code_id=tag,
            on_first_block=on_first_block,
        )
        return response, tag
    except Exception as e:
        await bomb_log(f"Gemini streaming call failed: {e}")
        # Fall back to non-streaming on error
        return await spark_gemini(txt, prompt_override=prompt_override)
