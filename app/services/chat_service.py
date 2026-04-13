from app.db.sqlite import get_connection
from app.rag.retriever import retrieve_context
from app.rag.prompt_builder import build_prompt
from app.rag.generator import generate_answer


def save_chat_interaction(user_message: str, bot_response: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO chat_logs (user_message, bot_response)
    VALUES (?, ?)
    """, (user_message, bot_response))

    conn.commit()
    conn.close()


def process_chat_message(message: str) -> str:
    context_chunks = retrieve_context(message, n_results=2)
    prompt = build_prompt(message, context_chunks)
    answer = generate_answer(prompt)

    save_chat_interaction(message, answer)
    return answer