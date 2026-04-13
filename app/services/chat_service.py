from app.db.sqlite import get_connection
from app.rag.retriever import retrieve_context
from app.rag.prompt_builder import build_prompt, detect_question_type, is_broad_question
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
    if is_broad_question(message):
        return "Hay muchas titulaciones en la Universidad CEU San Pablo. ¿Te interesa alguna facultad o área en concreto como Ingeniería, Medicina, Derecho o Empresa?"

    question_type = detect_question_type(message)
    n_results = 10 if question_type == "list" else 3

    context_chunks = retrieve_context(message, n_results=n_results)
    prompt = build_prompt(message, context_chunks)
    answer = generate_answer(prompt)

    save_chat_interaction(message, answer)
    return answer