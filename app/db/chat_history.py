from app.db.sqlite import get_connection


def save_message(session_id: str, role: str, message: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO chat_messages (session_id, role, message)
    VALUES (?, ?, ?)
    """, (session_id, role, message))

    conn.commit()
    conn.close()


def get_recent_messages(session_id: str, limit: int = 6) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT role, message, created_at
    FROM chat_messages
    WHERE session_id = ?
    ORDER BY id DESC
    LIMIT ?
    """, (session_id, limit))

    rows = cursor.fetchall()
    conn.close()

    messages = [dict(row) for row in rows]
    messages.reverse()
    return messages