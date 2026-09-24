import sqlite3
from config import DB_PATH


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            file_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()


# ---------- Kategoriyalar ----------

def add_category(name: str) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_categories():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM categories ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_category(category_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
    row = cur.fetchone()
    conn.close()
    return row


def delete_category(category_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM videos WHERE category_id = ?", (category_id,))
    cur.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    conn.commit()
    conn.close()


# ---------- Videolar ----------

def add_video(category_id: int, file_id: str, title: str, description: str = "") -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO videos (category_id, file_id, title, description) VALUES (?, ?, ?, ?)",
        (category_id, file_id, title, description),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_videos_by_category(category_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM videos WHERE category_id = ? ORDER BY id", (category_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_video(video_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM videos WHERE id = ?", (video_id,))
    row = cur.fetchone()
    conn.close()
    return row


def update_video_title(video_id: int, title: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE videos SET title = ? WHERE id = ?", (title, video_id))
    conn.commit()
    conn.close()


def update_video_description(video_id: int, description: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE videos SET description = ? WHERE id = ?", (description, video_id))
    conn.commit()
    conn.close()


def update_video_file(video_id: int, file_id: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE videos SET file_id = ? WHERE id = ?", (file_id, video_id))
    conn.commit()
    conn.close()


def delete_video(video_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM videos WHERE id = ?", (video_id,))
    conn.commit()
    conn.close()
