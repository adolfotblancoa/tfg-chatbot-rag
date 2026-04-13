def detect_question_type(user_question: str) -> str:
    question = user_question.lower()

    list_patterns = [
        "qué grados",
        "que grados",
        "cuáles son los grados",
        "cuales son los grados",
        "qué dobles grados",
        "que dobles grados",
        "qué titulaciones",
        "que titulaciones",
        "qué opciones hay",
        "que opciones hay",
        "qué carreras",
        "que carreras",
        "lista de",
        "dime los grados",
        "dime los dobles grados"
    ]

    if any(pattern in question for pattern in list_patterns):
        return "list"

    return "standard"

def is_broad_question(user_question: str) -> bool:
    question = user_question.lower().strip()

    broad_patterns = [
        "qué grados hay",
        "que grados hay",
        "qué carreras hay",
        "que carreras hay",
        "qué titulaciones hay",
        "que titulaciones hay",
        "toda la oferta",
        "todas las carreras",
        "todos los grados"
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
- No desarrolles una sola opción si el usuario está pidiendo varias.
- Si aparecen varias opciones, enuméralas de forma ordenada y limpia.
- Puedes usar una frase introductoria breve y después una lista separada por punto y coma.
- No inventes elementos que no aparezcan de forma clara.
- Nunca remitas al usuario a páginas, documentos, fragmentos o apartados.
- Si falta precisión o la lista puede no ser completa, ofrece continuar la conversación pidiendo la facultad o el área de interés.
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