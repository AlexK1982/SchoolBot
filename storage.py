import os
from urllib.parse import urlparse

import psycopg


DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL не найден")


def get_connection():
    return psycopg.connect(DATABASE_URL)


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    class_name TEXT NOT NULL
                )
            """)
        conn.commit()


def set_user_class(user_id, class_name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (user_id, class_name)
                VALUES (%s, %s)
                ON CONFLICT (user_id)
                DO UPDATE SET class_name = EXCLUDED.class_name
            """, (str(user_id), class_name))
        conn.commit()


def get_user_class(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT class_name
                FROM users
                WHERE user_id = %s
            """, (str(user_id),))
            row = cur.fetchone()

    if not row:
        return None

    return row[0]