import json

from app.db.chat_history import get_recent_messages, save_message
from app.db.rag_logs import save_rag_log
from app.rag.retriever import retrieve_context_with_metadata
from app.rag.prompt_builder import build_prompt, detect_question_type, is_broad_question
from app.rag.generator import generate_answer
from app.services.conversation_memory import reconstruct_user_query


def extract_documents_and_metadata(results: dict) -> tuple[list[str], str, str, str]:
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    sources = []
    pages = []
    chunks_info = []

    for doc, meta in zip(documents, metadatas):
        source = str(meta.get("source", ""))
        page = str(meta.get("page", ""))
        chunk_index = str(meta.get("chunk_index", ""))

        if source:
            sources.append(source)

        if page:
            pages.append(page)

        chunks_info.append({
            "source": source,
            "page": page,
            "chunk_index": chunk_index,
            "content": doc
        })

    unique_sources = ", ".join(sorted(set(sources)))
    unique_pages = ", ".join(sorted(set(pages), key=lambda x: int(x) if x.isdigit() else x))

    return (
        documents,
        unique_sources,
        unique_pages,
        json.dumps(chunks_info, ensure_ascii=False)
    )


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
            bot_response=answer,
            sources="",
            pages="",
            retrieved_chunks=""
        )

        return answer

    question_type = detect_question_type(effective_message)
    n_results = 10 if question_type == "list" else 3

    retrieval_results = retrieve_context_with_metadata(
        effective_message,
        n_results=n_results
    )

    context_chunks, sources, pages, retrieved_chunks = extract_documents_and_metadata(
        retrieval_results
    )

    prompt = build_prompt(effective_message, context_chunks)
    answer = generate_answer(prompt)

    save_message(session_id, "user", message)
    save_message(session_id, "assistant", answer)

    save_rag_log(
        session_id=session_id,
        original_message=message,
        effective_message=effective_message,
        question_type=question_type,
        bot_response=answer,
        sources=sources,
        pages=pages,
        retrieved_chunks=retrieved_chunks
    )

    return answer