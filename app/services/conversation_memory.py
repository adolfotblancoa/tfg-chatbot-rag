from app.rag.prompt_builder import normalize_question


def is_short_followup(message: str) -> bool:
    normalized = normalize_question(message)
    word_count = len(normalized.split())

    short_answers = {
        "ingenieria", "medicina", "farmacia", "derecho",
        "empresa", "economicas", "eps",
        "si", "no", "bilingue", "espanol", "ingles"
    }

    return word_count <= 4 or normalized in short_answers or normalized.startswith("y ")


def detect_intent(message: str) -> str | None:
    text = normalize_question(message)

    if "doble" in text and "grado" in text:
        return "dobles_grados"

    if "grado" in text or "carrera" in text or "titulacion" in text:
        return "grados"

    if "idioma" in text or "bilingue" in text or "ingles" in text:
        return "idiomas"

    if "campus" in text or "donde esta" in text or "ubicacion" in text:
        return "campus"

    if "practica" in text or "practicas" in text:
        return "practicas"

    return None


def extract_area(message: str) -> str:
    text = normalize_question(message)

    areas = {
        "ingenieria": ["ingenieria", "eps", "informatica", "telecomunicacion", "arquitectura"],
        "medicina": ["medicina", "enfermeria", "fisioterapia", "odontologia", "psicologia", "genetica"],
        "farmacia": ["farmacia", "biotecnologia", "nutricion", "optica"],
        "derecho": ["derecho", "juridico", "abogacia"],
        "economia": ["economia", "economicas", "empresa", "ade", "finanzas"]
    }

    for area, keywords in areas.items():
        if any(keyword in text for keyword in keywords):
            return area

    return message.strip()


def get_last_user_intent(recent_messages: list[dict]) -> str | None:
    for msg in reversed(recent_messages):
        if msg["role"] == "user":
            intent = detect_intent(msg["message"])
            if intent:
                return intent

    return None


def reconstruct_user_query(current_message: str, recent_messages: list[dict]) -> str:
    current = current_message.strip()

    if not recent_messages:
        return current

    if not is_short_followup(current):
        return current

    last_intent = get_last_user_intent(recent_messages)
    area = extract_area(current)

    if last_intent == "dobles_grados":
        return f"¿Qué dobles grados hay en {area}?"

    if last_intent == "grados":
        return f"¿Qué grados hay en {area}?"

    if last_intent == "idiomas":
        return f"¿Qué idiomas ofrece {area}?"

    if last_intent == "campus":
        return f"¿Dónde está el campus de {area}?"

    if last_intent == "practicas":
        return f"¿Qué prácticas ofrece {area}?"

    return current