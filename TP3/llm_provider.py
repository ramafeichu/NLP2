# llm_provider.py
import os
import requests
from typing import List, Dict, Optional

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

def generate_chat_completion(messages: List[Dict[str, str]], temperature: float = 0.2, max_tokens: int = 512) -> str:
    """
    Llama al endpoint OpenAI-compatible de Groq para generar una respuesta.
    Requiere GROQ_API_KEY en el .env. Si no está, lanza un RuntimeError.
    """
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY no está configurada. "
            "Defínela en tu .env o modifica llm_provider.py para otro backend."
        )

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()
