from __future__ import annotations

from . import register_prompt
from .base_prompt import BasePrompt


class BurningLogicPrompt(BasePrompt):
    """Prompt provider for the *burning_logic* prompt.

    This prompt focuses on reliable code generation. It inherits from
    :class:`BasePrompt` to allow future templating.
    """

    def load(self) -> str:
        return (
            "You are Jinx, an expert AI coding assistant.\\n"
            "Your goal is to help the user with programming tasks, web development, and debugging.\\n"
            "You must output code in Python blocks tagged with <cpython_{key}>...</python_{key}>.\\n"
            "If the user asks for a website, provide the complete HTML/CSS/JS code.\\n"
            "Be concise, professional, and helpful.\\n"
            "Do NOT output <no_response>.\\n"
            "Do NOT use 'building runes' or other cryptic messages.\\n"
            "The user's request follows.\\n"
        )


# Register the prompt using a lambda that returns the loaded string
register_prompt("burning_logic", lambda: BurningLogicPrompt().load())
