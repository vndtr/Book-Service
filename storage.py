import json
import os
from typing import List

from models.book import Book
from models.user import User

DATA_DIR = "data"
BOOKS_FILE = os.path.join(DATA_DIR, "books.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")


def ensure_data_dir() -> None:
    """Создать каталог для данных, если его нет."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_books(filename: str = BOOKS_FILE) -> List[Book]:
    """Загрузить книги из JSON-файла в виде объектов Book."""
    ensure_data_dir()
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        return [Book.from_dict(item) for item in data]
    except (json.JSONDecodeError, OSError) as e:
        print(f"Ошибка загрузки книг: {e}")
        return []


def save_books(books: List[Book], filename: str = BOOKS_FILE) -> None:
    """Сохранить книги в JSON-файл."""
    ensure_data_dir()
    try:
        data = [book.to_dict() for book in books]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"Ошибка сохранения данных: {e}")


def load_users(filename: str = USERS_FILE) -> List[User]:
    """Загрузить пользователей из JSON-файла."""
    ensure_data_dir()
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        return [User.from_dict(item) for item in data]
    except (json.JSONDecodeError, OSError) as e:
        print(f"Ошибка загрузки пользователей: {e}")
        return []


def save_users(users: List[User], filename: str = USERS_FILE) -> None:
    """Сохранить пользователей в JSON-файл."""
    ensure_data_dir()
    try:
        data = [user.to_dict() for user in users]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"Ошибка сохранения пользователей: {e}")
