from __future__ import annotations

async def build_header_and_tag(prompt_override: str | None = None) -> tuple[str, str]:
    """Generate a unique code tag and standard instruction header."""
    import uuid
    tag = str(uuid.uuid4())[:8]
    
    # Basic system prompt / header
    header = (
        f"You are Jinx, an advanced AI coding agent.\n"
        f"You must output code in Python blocks tagged with <python_{tag}>...</python_{tag}>.\n"
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
