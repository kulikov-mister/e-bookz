import sqlite3

DB_NAME = "users.db"


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT,
            bot_token TEXT
        )
        """)
        conn.commit()


def set_user_language(user_id, language):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO users (user_id, language) VALUES (?, ?)", (user_id, language))
        conn.commit()


def get_user_language(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
        row = cursor.fetchone()
        if row:
            return row[0]
        return None


def set_user_token(user_id, token):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET bot_token=? WHERE user_id=?", (token, user_id))
        conn.commit()


init_db()