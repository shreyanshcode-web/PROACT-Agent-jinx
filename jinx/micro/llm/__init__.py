from __future__ import annotations

import os
from .gemini_caller import call_gemini
from .gemini_service import spark_gemini, spark_gemini_streaming

# For backward compatibility
try:
    from .openai_caller import call_openai
except ImportError:
    call_openai = None

# Set default provider based on environment variable or default to Gemini
DEFAULT_PROVIDER = os.getenv("JINX_LLM_PROVIDER", "gemini").lower()

if DEFAULT_PROVIDER == "gemini":
    call_llm = call_gemini
    spark_llm = spark_gemini
    spark_llm_streaming = spark_gemini_streaming
else:
    call_llm = call_openai
    spark_llm = None  # You'll need to import the OpenAI spark functions if needed
    spark_llm_streaming = None

__all__ = [
    "call_llm",
    "spark_llm",
    "spark_llm_streaming",
    "call_gemini",
    "spark_gemini",
    "spark_gemini_streaming",
]
