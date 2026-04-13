from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)


def clean_response(text: str) -> str:
    text = text.replace("\\n", " ")
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text.strip()


def generate_answer(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return clean_response(response.output_text)