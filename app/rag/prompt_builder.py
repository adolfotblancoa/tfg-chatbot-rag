def normalize_question(text: str) -> str:
    text = text.lower().strip()
    replacements = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return " ".join(text.split())


def detect_question_type(user_question: str) -> str:
    question = normalize_question(user_question)

    list_patterns = [
        "que grados",
        "cuales son los grados",
        "que dobles grados",
        "que doble grados",
        "que titulaciones",
        "que opciones hay",
        "que carreras",
        "lista de",
        "dime los grados",
        "dime los dobles grados",
        "dime los doble grados"
    ]

    if any(pattern in question for pattern in list_patterns):
        return "list"

    return "standard"


def is_broad_question(user_question: str) -> bool:
    question = normalize_question(user_question)

    broad_patterns = [
        "que grados hay",
        "que carreras hay",
        "que titulaciones hay",
        "toda la oferta",
        "todas las carreras",
        "todos los grados",
        "que dobles grados hay",
        "que doble grados hay"
    ]

    return question in broad_patterns

def build_prompt(user_question: str, context_chunks: list[str]) -> str:
    context_text = "\n\n---\n\n".join(context_chunks)
    question_type = detect_question_type(user_question)

    if question_type == "list":
        instructions = """
Eres un asistente institucional de la Universidad CEU San Pablo.

Responde únicamente con la información disponible en los fragmentos proporcionados.

Instrucciones:
- El usuario está pidiendo una lista de grados, dobles grados, titulaciones u opciones.
- Tu prioridad es enumerar las opciones que aparezcan claramente en los fragmentos.
- Responde de forma natural, clara y directa.
- No menciones el contexto, los fragmentos, ni expliques cómo has obtenido la información.
- No digas frases como "según el contexto", "la información proporcionada" o similares.
- No remitas al usuario a páginas, documentos, apartados o fragmentos.
- No desarrolles una sola opción si el usuario está pidiendo varias.
- Si aparecen varias opciones, enuméralas de forma ordenada y limpia.
- Puedes usar una frase introductoria breve y después una lista separada por punto y coma.
- No inventes elementos que no aparezcan de forma clara.
- Si falta precisión o no puedes asegurar que la lista esté completa, termina con una frase breve y conversacional como: "Puedo concretarte más si me indicas el grado, la facultad o el área que te interesa."
- No uses markdown.
- Evita explicaciones largas.
"""
    else:
        instructions = """
Eres un asistente institucional de la Universidad CEU San Pablo.
Tu tarea es responder preguntas de futuros alumnos utilizando únicamente la información contenida en los fragmentos proporcionados.

Instrucciones:
- Responde de forma clara, natural, precisa y útil.
- No copies literalmente tablas, listados o fragmentos salvo que sea imprescindible.
- Resume y reformula la información para que la respuesta suene natural.
- Utiliza toda la información proporcionada y selecciona la más relevante.
- Si la respuesta requiere combinar varios fragmentos, intégralos de forma coherente.
- Prioriza siempre la información más específica y directamente relacionada con la pregunta.
- Evita incluir información irrelevante o redundante.
- No inventes información ni añadas datos que no aparezcan en los fragmentos.
- Si no hay información suficiente para responder con seguridad, indícalo de forma breve y natural.
- Si la pregunta es ambigua, acláralo brevemente en la respuesta.
- No uses formato markdown.
- No uses viñetas salvo que la pregunta pida explícitamente una lista.
- Evita saltos de línea innecesarios.
"""

    prompt = f"""
{instructions}

Fragmentos:
{context_text}

Pregunta del usuario:
{user_question}

Respuesta:
""".strip()

    return prompt