import uuid
from app.db.sqlite import get_connection


def get_or_create_session(user_identifier: str, channel: str) -> str:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT session_id
    FROM sessions
    WHERE user_identifier = ? AND channel = ?
    ORDER BY last_interaction_at DESC
    LIMIT 1
    """, (user_identifier, channel))

    row = cursor.fetchone()

    if row:
        session_id = row["session_id"]

        cursor.execute("""
        UPDATE sessions
        SET last_interaction_at = CURRENT_TIMESTAMP
        WHERE session_id = ?
        """, (session_id,))

        conn.commit()
        conn.close()
        return session_id

    session_id = str(uuid.uuid4())

    cursor.execute("""
    INSERT INTO sessions (session_id, user_identifier, channel)
    VALUES (?, ?, ?)
    """, (session_id, user_identifier, channel))

    conn.commit()
    conn.close()

    return session_id