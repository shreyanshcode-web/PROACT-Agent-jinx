from __future__ import annotations

from typing import Any, Dict

# Note: RAG/File Search was an OpenAI-specific feature.
# For Gemini, we use embeddings and semantic search instead.
# This module is kept for backward compatibility but returns empty configs.

from jinx.settings import Settings


def build_file_search_tools() -> Dict[str, Any]:
    """Compatibility stub for File Search tool binding.
    
    Returns empty dict as Gemini doesn't use OpenAI's file search tools.
    Use embeddings-based semantic search instead.
    """
    return {}


def build_file_search_tools_from_settings(settings: Settings) -> Dict[str, Any]:
    """Compatibility stub for File Search from Settings.
    
    Returns empty dict as Gemini doesn't use OpenAI's file search tools.
    Use embeddings-based semantic search instead.
    """
    return {}


__all__ = [
    "build_file_search_tools",
    "build_file_search_tools_from_settings",
]
