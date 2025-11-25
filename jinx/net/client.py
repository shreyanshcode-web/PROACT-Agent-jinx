from __future__ import annotations

"""Network client facade.

Delegates to the micro-module implementation under
`jinx.micro.net.client` while keeping the public API stable.
Uses Gemini for LLM operations.
"""

from jinx.micro.net.client import (
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
