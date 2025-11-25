from __future__ import annotations

from .client import (
    get_gemini_client,
    get_openai_client,  # Backward compatibility
    prewarm_gemini_client,
    prewarm_openai_client,  # Backward compatibility
)


__all__ = [
    "get_gemini_client",
    "get_openai_client",  # Backward compatibility
    "prewarm_gemini_client",
    "prewarm_openai_client",  # Backward compatibility
]
