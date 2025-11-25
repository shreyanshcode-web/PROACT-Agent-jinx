from __future__ import annotations

import asyncio
import os
from typing import Any, Optional, Callable, Dict
import google.generativeai as genai
from jinx.logging_service import bomb_log
from jinx.micro.rag.file_search import build_file_search_tools
from .llm_cache import call_openai_cached, call_openai_multi_validated
from jinx.micro.text.heuristics import is_code_like as _is_code_like
import asyncio as _asyncio
import queue as _queue

# Initialize Gemini client
GEMINI_MODEL = "gemini-2.0-flash"  # or "gemini-1.5-pro" when available

def get_gemini_client():
    """Get or initialize the Gemini client with API key."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    genai.configure(api_key=api_key)
    return genai

async def call_gemini(instructions: str, model: str, input_text: str) -> str:
    """Call Gemini API and return output text."""
    try:
        if not (os.getenv("GEMINI_API_KEY") or ""):
            await bomb_log("GEMINI_API_KEY missing; LLM disabled — returning stub output")
            return (
                "<llm_disabled>\n"
                "No Gemini API key configured. Set GEMINI_API_KEY in .env to enable model calls.\n"
                "</llm_disabled>"
            )
            
        client = get_gemini_client()
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        # Combine instructions and input text for Gemini's chat format
        prompt = f"{instructions}\n\n{input_text}"
        
        response = await asyncio.to_thread(
            model.generate_content,
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 2048,
            }
        )
        
        return response.text
        
    except Exception as e:
        await bomb_log(f"ERROR Gemini API call failed: {e}")
        raise

async def call_gemini_validated(instructions: str, model: str, input_text: str, *, code_id: str) -> str:
    """Call Gemini with validation and caching."""
    # For now, just call the regular function
    # In a real implementation, you might want to add validation logic here
    return await call_gemini(instructions, model, input_text)

async def call_gemini_stream_first_block(
    instructions: str,
    model: str,
    input_text: str,
    *,
    code_id: str,
    on_first_block: Optional[Callable[[str], None]] = None,
) -> str:
    """Stream Gemini response and fire callback on first complete code block."""
    try:
        client = get_gemini_client()
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        # Combine instructions and input text for Gemini's chat format
        prompt = f"{instructions}\n\n{input_text}"
        
        # For streaming, we'll collect chunks and look for the first code block
        full_response = ""
        code_block_tag = f"<python_{code_id}>"
        code_block_found = False
        
        # Note: Gemini's Python SDK doesn't support streaming in the same way as OpenAI
        # This is a simplified implementation that processes the full response
        response = await asyncio.to_thread(
            model.generate_content,
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 2048,
            }
        )
        
        full_response = response.text
        
        # Look for the first code block
        if code_block_tag in full_response and on_first_block:
            # Extract the first code block
            start_idx = full_response.find(code_block_tag) + len(code_block_tag)
            end_tag = f"</python_{code_id}>"
            end_idx = full_response.find(end_tag, start_idx)
            
            if end_idx != -1:
                code_block = full_response[start_idx:end_idx].strip()
                on_first_block(code_block)
        
        return full_response
        
    except Exception as e:
        await bomb_log(f"ERROR Gemini streaming failed: {e}")
        # Fall back to non-streaming on error
        return await call_gemini(instructions, model, input_text)
