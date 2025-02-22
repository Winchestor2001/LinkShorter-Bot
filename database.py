import sqlite3
import shortuuid

DB_PATH = "database.db"


class Database:
    def __init__(self):
        """Создаёт таблицу, если её нет"""
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS links (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    short TEXT UNIQUE,
                    original TEXT UNIQUE
                )
            """)
            conn.commit()

    def get_original_url(self, short_code: str) -> str | None:
        """Получает оригинальный URL по короткому коду"""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT original FROM links WHERE short = ?", (short_code,))
            result = cursor.fetchone()
        return result[0] if result else None

    def create_short_url(self, original_url: str) -> str:
        """Создаёт короткую ссылку или возвращает существующую"""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            # Проверяем, существует ли уже такая ссылка
            cursor.execute("SELECT short FROM links WHERE original = ?", (original_url,))
            existing = cursor.fetchone()
            if existing:
                return existing[0]

            # Генерируем новый короткий код
            short_code = shortuuid.uuid()[:6]
            cursor.execute("INSERT INTO links (short, original) VALUES (?, ?)", (short_code, original_url))
            conn.commit()
            return short_code
