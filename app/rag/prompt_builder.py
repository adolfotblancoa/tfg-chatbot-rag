def build_prompt(user_question: str, context_chunks: list[str]) -> str:
    context_text = "\n\n".join(context_chunks)

    prompt = f"""
Eres un asistente institucional del CEU.
Responde únicamente con la información proporcionada en el contexto.
Si la respuesta no está en el contexto, indica claramente que no dispones de esa información.
Responde de forma clara, breve y útil.

Contexto:
{context_text}

Pregunta del usuario:
{user_question}
"""
    return prompt.strip()