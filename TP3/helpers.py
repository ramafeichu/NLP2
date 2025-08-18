from typing import List, Optional
import unicodedata
import re

def _strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )

def _select_target_from_messages(messages: List[dict], possibilities: List) -> Optional[str]:
    """
    Mira el último mensaje del usuario y decide 'ana' o 'juan' si lo menciona.
    También acepta patrones tipo '@ana', 'para Juan', etc.
    """
    if not messages:
        return None

    # Tomamos el último mensaje del usuario (si existe)
    user_msgs = [m for m in messages if m.get("role") == "user"]
    if not user_msgs:
        return None

    text = user_msgs[-1].get("content", "")
    norm = _strip_accents(text).lower()

    # Patrones simples (mencion directa o palabras cercanas)
    for persona in possibilities:
        p = _strip_accents(persona).lower()
        # coincide 'ana', 'juan', '@ana', 'para juan', etc.
        if re.search(rf"(?:^|\W)@?{p}(?:\W|$)", norm):
            return persona

    return None
