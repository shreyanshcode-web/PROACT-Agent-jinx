from __future__ import annotations

import os
from typing import Any


_gemini_client: Any | None = None


def get_gemini_client() -> Any:
    """Return a singleton Gemini client.
    
    This replaces the OpenAI client entirely with Gemini.
    """
    global _gemini_client
    if _gemini_client is not None:
        return _gemini_client
    
    # Check if Gemini API key is available
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Return a dummy client that will raise an error with a helpful message
        class DummyClient:
            def __getattr__(self, name):
                raise Exception(
                    "Gemini API key not configured. "
                    "Please set GEMINI_API_KEY environment variable in your .env file"
                )
        _gemini_client = DummyClient()
        return _gemini_client
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        _gemini_client = genai
        return _gemini_client
    except ImportError:
        raise Exception(
            "google-generativeai package not installed. "
            "Run: pip install google-generativeai"
        )


# Keep the old function name for backward compatibility
def get_openai_client() -> Any:
    """Backward compatibility wrapper - returns Gemini client."""
    return get_gemini_client()


def prewarm_gemini_client() -> None:
    """Instantiate the Gemini client early.
    
    Safe to call multiple times; returns immediately if already initialized.
    """
    try:
        _ = get_gemini_client()
    except Exception:
        # Best-effort: swallow errors — prewarm should never crash startup
        pass


# Backward compatibility
prewarm_openai_client = prewarm_gemini_client


__all__ = [
    "get_gemini_client",
    "get_openai_client",  # Backward compatibility
    "prewarm_gemini_client",
    "prewarm_openai_client",  # Backward compatibility
]
