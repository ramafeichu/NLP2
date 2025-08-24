from typing import List, Optional, Dict
import unicodedata
import re


def strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def select_target_from_messages(messages: List[dict], possibilities: List) -> Optional[str]:
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
    norm = strip_accents(text).lower()

    # Patrones simples (mencion directa o palabras cercanas)
    for persona in possibilities:
        p = strip_accents(persona).lower()
        # coincide 'ana', 'juan', '@ana', 'para juan', etc.
        if re.search(rf"(?:^|\W)@?{p}(?:\W|$)", norm):
            return persona

    return None


def extract_system_last_message(messages: List[Dict]) -> Optional[str]:
    return extract_role_last_message(messages, "system")


def extract_user_last_message(messages: List[Dict]) -> Optional[str]:
    return extract_role_last_message(messages, "user")


def extract_role_last_message(messages: List[Dict], role: str) -> Optional[str]:
    user_msgs = [m for m in messages if m.get("role") == role]
    return user_msgs[-1]["content"] if user_msgs else None


def build_prompt_messages(persona: str, user_input: str, context_chunks: List[str]) -> List[Dict[str, str]]:
    """
    Builds the chat payload for the LLM:
    - system: instructions + context
    - user: the original question
    """
    context_text = "\n\n".join(context_chunks).strip() if context_chunks else ""
    system_content = (
        f"You are a knowledge assistant for {persona}. "
        f"Use ONLY the provided context to answer. "
        f"If the answer is not in the context, explicitly say that there isn't enough information.\n\n"
        f"=== CONTEXT ===\n{context_text}\n"
        f"================\n"
    )
    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_input},
    ]



