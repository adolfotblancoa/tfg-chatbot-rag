from app.db.sqlite import get_connection


def generate_dummy_response(message: str) -> str:
    return f"Has dicho: {message}"


def save_chat_interaction(user_message: str, bot_response: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO chat_logs (user_message, bot_response)
    VALUES (?, ?)
    """, (user_message, bot_response))

    conn.commit()
    conn.close()