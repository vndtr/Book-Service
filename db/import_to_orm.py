import os
import sys
import sqlite3
import json
from pathlib import Path
import django

# Настройка путей
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book_service.settings")
django.setup()

# Импорты ниже django.setup() - это нормально для скриптов Django (noqa)
from users.models import User  # noqa: E402
from books.models import Book  # noqa: E402

SOURCE_DB = BASE_DIR / "data" / "library.sqlite"
USERS_FILE = BASE_DIR / "data" / "users.json"


def get_row_value(row, key, default=""):
    """Безопасно получает значение из sqlite3.Row или возвращает default."""
    if key in row.keys():
        return row[key]
    return default


def main():
    # 1. Переносим пользователей (из старой базы или JSON)
    if SOURCE_DB.exists():
        with sqlite3.connect(SOURCE_DB) as conn:
            conn.row_factory = sqlite3.Row
            users = conn.execute("SELECT * FROM users").fetchall()
            for row in users:
                User.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                        "created_at": get_row_value(row, "created_at", "")
                    }
                )
    elif USERS_FILE.exists():
        with open(USERS_FILE, encoding="utf-8") as f:
            users = json.load(f)
            for row in users:
                User.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                        "created_at": row.get("created_at", "")
                    }
                )

    # 2. Переносим книги
    if SOURCE_DB.exists():
        with sqlite3.connect(SOURCE_DB) as conn:
            conn.row_factory = sqlite3.Row
            books = conn.execute("SELECT * FROM books").fetchall()
            for row in books:
                try:
                    user_obj = User.objects.get(pk=row["user_id"])
                    Book.objects.update_or_create(
                        pk=row["id"],
                        defaults={
                            "title": row["title"],
                            "author": row["author"],
                            "year": row["year"],
                            "status": row["status"],
                            "date_added": get_row_value(
                                row, "date_added", ""
                            ),
                            "user": user_obj
                        }
                    )
                except User.DoesNotExist:
                    msg = f"Пропущена книга ID {row['id']}: нет юзера"
                    print(msg)

    print(f"Пользователей: {User.objects.count()}")
    print(f"Книг: {Book.objects.count()}")


if __name__ == "__main__":
    main()
