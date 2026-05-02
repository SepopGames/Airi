import sqlite3
from datetime import datetime
from pathlib import Path


# Корень проекта: папка airi_jarvis.
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Путь к папке data и файлу базы данных.
DATA_DIR = PROJECT_DIR / "data"
DB_PATH = DATA_DIR / "memory.sqlite"


def init_db():
    # Создаем папку data, если ее еще нет.
    DATA_DIR.mkdir(exist_ok=True)

    # Подключаемся к SQLite-базе. Если файла нет, sqlite3 создаст его сам.
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        # Создаем таблицу memories, если она еще не существует.
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        # Сохраняем изменения в базе данных.
        connection.commit()


def add_memory(text: str):
    # На всякий случай подготавливаем базу перед добавлением записи.
    init_db()

    # Сохраняем дату создания в простом текстовом формате ISO.
    created_at = datetime.now().isoformat(timespec="seconds")

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        # Добавляем новое воспоминание в таблицу.
        cursor.execute(
            "INSERT INTO memories (text, created_at) VALUES (?, ?)",
            (text, created_at),
        )

        connection.commit()


def get_recent_memories(limit: int = 5):
    # На всякий случай подготавливаем базу перед чтением.
    init_db()

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        # Берем последние N записей: сначала самые новые.
        cursor.execute(
            "SELECT text FROM memories ORDER BY id DESC LIMIT ?",
            (limit,),
        )

        rows = cursor.fetchall()

    # Возвращаем только текст воспоминаний списком строк.
    return [row[0] for row in rows]
