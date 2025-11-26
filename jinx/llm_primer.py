from __future__ import annotations

async def build_header_and_tag(prompt_override: str | None = None) -> tuple[str, str]:
    """Generate a unique code tag and standard instruction header."""
    import uuid
    tag = str(uuid.uuid4())[:8]
    
    # Simple, direct system prompt
    header = (
        f"You are Jinx, an expert AI coding assistant.\n"
        f"Your goal is to help the user with programming tasks, web development, and debugging.\n"
        f"You must output code in Python blocks tagged with <python_{tag}>...</python_{tag}>.\n"
        f"If the user asks for a website, provide the complete HTML/CSS/JS code.\n"
        f"Be concise, professional, and helpful.\n"
        f"Do NOT output <no_response>.\n"
        f"The user's request follows.\n"
    )
    
    if prompt_override:
        header += f"\nNote: {prompt_override}\n"
        
    return header, tag


async def code_primer(prompt_override: str | None = None) -> tuple[str, str]:
    """Build instruction header and return it with a code tag identifier.

    Returns (header_plus_prompt, code_tag_id).
    """
    return await build_header_and_tag(prompt_override)
