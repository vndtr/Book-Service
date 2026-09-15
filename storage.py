"""Сохранение и загрузка данных проекта в JSON."""

import json
import os
from typing import List


DATA_DIR = "data"
BOOKS_FILE = os.path.join(DATA_DIR, "books.json")


def ensure_data_dir() -> None:
    """Создать каталог для данных, если его нет."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_books(filename: str = BOOKS_FILE) -> List[dict]:
    """Загрузить книги из JSON-файла."""
    ensure_data_dir()
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError) as e:
        print(f"Ошибка загрузки данных: {e}")
        return []


def save_books(books: List[dict], filename: str = BOOKS_FILE) -> None:
    """Сохранить книги в JSON-файл."""
    ensure_data_dir()
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"Ошибка сохранения данных: {e}")