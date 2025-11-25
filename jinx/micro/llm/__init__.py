from __future__ import annotations

from .gemini_caller import call_gemini
from .gemini_service import spark_gemini, spark_gemini_streaming

# Default to Gemini for all LLM operations
call_llm = call_gemini
spark_llm = spark_gemini
spark_llm_streaming = spark_gemini_streaming

__all__ = [
    "call_llm",
    "spark_llm",
    "spark_llm_streaming",
    "call_gemini",
    "spark_gemini",
    "spark_gemini_streaming",
]
