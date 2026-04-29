from app.db.chat_history import get_recent_messages, save_message
from app.db.rag_logs import save_rag_log
from app.rag.retriever import retrieve_context
from app.rag.prompt_builder import build_prompt, detect_question_type, is_broad_question
from app.rag.generator import generate_answer
from app.services.conversation_memory import reconstruct_user_query


def process_chat_message(session_id: str, message: str) -> str:
    recent_messages = get_recent_messages(session_id=session_id, limit=6)

    effective_message = reconstruct_user_query(
        current_message=message,
        recent_messages=recent_messages
    )

    if is_broad_question(effective_message):
        question_type = "broad"
        answer = (
            "Hay muchos grados y dobles grados en distintas facultades. "
            "¿Te interesa alguna área en concreto como Ingeniería, Medicina, "
            "Farmacia, Derecho o Empresa?"
        )

        save_message(session_id, "user", message)
        save_message(session_id, "assistant", answer)

        save_rag_log(
            session_id=session_id,
            original_message=message,
            effective_message=effective_message,
            question_type=question_type,
            bot_response=answer
        )

        return answer

    question_type = detect_question_type(effective_message)
    n_results = 10 if question_type == "list" else 3

    context_chunks = retrieve_context(effective_message, n_results=n_results)
    prompt = build_prompt(effective_message, context_chunks)
    answer = generate_answer(prompt)

    save_message(session_id, "user", message)
    save_message(session_id, "assistant", answer)

    save_rag_log(
        session_id=session_id,
        original_message=message,
        effective_message=effective_message,
        question_type=question_type,
        bot_response=answer
    )

    return answer