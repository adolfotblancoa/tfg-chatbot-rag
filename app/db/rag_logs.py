from app.db.sqlite import get_connection


def save_rag_log(
    session_id: str,
    original_message: str,
    effective_message: str,
    question_type: str,
    bot_response: str
) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO rag_logs (
        session_id,
        original_message,
        effective_message,
        question_type,
        bot_response
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        session_id,
        original_message,
        effective_message,
        question_type,
        bot_response
    ))

    conn.commit()
    conn.close()