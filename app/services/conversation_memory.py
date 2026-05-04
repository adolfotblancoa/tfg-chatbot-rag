from app.rag.prompt_builder import normalize_question


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

    if "practica" in text:
        return "practicas"

    return None


def is_followup_message(message: str) -> bool:
    text = normalize_question(message)

    if text.startswith("y "):
        return True

    if text.startswith("en "):
        return True

    if text.startswith("el de ") or text.startswith("la de "):
        return True

    known_short_answers = {
        "ingenieria", "medicina", "farmacia", "derecho",
        "empresa", "economia", "economicas", "educacion",
        "eps", "informatica", "izquierdo", "derecho"
    }

    if text in known_short_answers:
        return True

    word_count = len(text.split())

    if word_count <= 3 and detect_intent(text) is None:
        return True

    return False