from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)


def format_history(recent_messages: list[dict]) -> str:
    lines = []

    for msg in recent_messages:
        role = "Usuario" if msg["role"] == "user" else "Asistente"
        lines.append(f"{role}: {msg['message']}")

    return "\n".join(lines)


def rewrite_query_with_context(current_message: str, recent_messages: list[dict]) -> str:
    history_text = format_history(recent_messages)

    prompt = f"""
Eres un reformulador de consultas para un chatbot universitario.

Tu tarea es convertir el mensaje actual del usuario en una pregunta completa y autónoma, usando el historial reciente de conversación.

Reglas:
- No respondas a la pregunta.
- Solo devuelve la pregunta reformulada.
- Si el mensaje actual ya es claro e independiente, devuélvelo igual.
- Si el mensaje actual depende del contexto anterior, complétalo con la intención adecuada.
- No inventes datos de la universidad.
- Mantén el idioma español.

Historial:
{history_text}

Mensaje actual:
{current_message}

Pregunta reformulada:
""".strip()

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text.strip()