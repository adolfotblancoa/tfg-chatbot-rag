def is_short_followup(message: str) -> bool:
    normalized = message.strip().lower()
    word_count = len(normalized.split())

    short_answers = {
        "ingenieria", "ingeniería", "medicina", "farmacia", "derecho",
        "empresa", "economicas", "económicas", "eps",
        "si", "sí", "no", "bilingue", "bilingüe", "español", "ingles", "inglés"
    }

    return word_count <= 3 or normalized in short_answers


def reconstruct_user_query(current_message: str, recent_messages: list[dict]) -> str:
    if not recent_messages:
        return current_message

    current = current_message.strip()

    if not is_short_followup(current):
        return current

    last_assistant_message = None
    for msg in reversed(recent_messages):
        if msg["role"] == "assistant":
            last_assistant_message = msg["message"]
            break

    if not last_assistant_message:
        return current

    assistant_lower = last_assistant_message.lower()
    current_lower = current.lower()

    if "area" in assistant_lower or "facultad" in assistant_lower:
        return f"¿Qué grados de {current} hay?"

    if "idioma" in assistant_lower:
        return f"¿Qué idiomas ofrece {current}?"

    if "dobles grados" in assistant_lower:
        return f"¿Qué dobles grados hay en {current}?"

    return current