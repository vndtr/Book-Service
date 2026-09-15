"""Функции для работы с книгами."""

from datetime import date
from typing import Optional

STATUS_WANT_TO_READ = "хочу прочитать"
STATUS_READING = "читаю"
STATUS_READ = "прочитано"
STATUS_ON_HOLD = "отложено"

ALL_STATUSES = [
    STATUS_WANT_TO_READ,
    STATUS_READING,
    STATUS_READ,
    STATUS_ON_HOLD,
]


def get_status_display(status: str) -> str:
    """Вернуть читаемое название статуса."""
    if status == STATUS_READ:
        return "Прочитано"
    elif status == STATUS_READING:
        return "Читаю"
    elif status == STATUS_WANT_TO_READ:
        return "Хочу прочитать"
    elif status == STATUS_ON_HOLD:
        return "Отложено"
    return "Неизвестный статус"


def add_book(
    books: list[dict],
    title: str,
    author: str,
    year: int,
    status: str
) -> dict:
    """Добавить книгу в список books и вернуть её словарь."""
    book_id = len(books) + 1
    book = {
        "id": book_id,
        "title": title,
        "author": author,
        "year": year,
        "status": status,
        "date_added": date.today().strftime("%d.%m.%Y"),
    }
    books.append(book)
    return book


def find_books(books: list[dict], query: str) -> list[dict]:
    """Найти книги по подстроке в названии или авторе."""
    query_lower = query.lower()
    result = []
    for book in books:
        if (query_lower in book["title"].lower()
                or query_lower in book["author"].lower()):
            result.append(book)
    return result


def find_book_by_id(books: list[dict], book_id: int) -> Optional[dict]:
    """Найти книгу по идентификатору."""
    for book in books:
        if book["id"] == book_id:
            return book
    return None


def filter_books_by_status(books: list[dict], status: str) -> list[dict]:
    """Отобрать книги по статусу (генератор)."""
    return [book for book in books if book["status"] == status]


def count_books_by_status(books: list[dict], status: str) -> int:
    """Подсчитать количество книг с заданным статусом."""
    return sum(1 for book in books if book["status"] == status)


def sort_books_by_title(books: list[dict]) -> list[dict]:
    """Отсортировать книги по названию (lambda-функция)."""
    return sorted(books, key=lambda book: book["title"].lower())


def sort_books_by_year(books: list[dict]) -> list[dict]:
    """Отсортировать книги по году издания."""
    return sorted(books, key=lambda book: book["year"])


def change_status(books: list[dict], book_id: int, new_status: str) -> bool:
    """Изменить статус книги. Вернуть True при успехе."""
    book = find_book_by_id(books, book_id)
    if book is None:
        return False
    book["status"] = new_status
    return True


def remove_book(books: list[dict], book_id: int) -> Optional[dict]:
    """Удалить книгу по идентификатору. Вернуть удалённую книгу."""
    for i, book in enumerate(books):
        if book["id"] == book_id:
            return books.pop(i)
    return None


def get_statistics(books: list[dict]) -> dict:
    """Вернуть статистику по книгам."""
    total = len(books)
    stats = {
        "total": total,
        "by_status": {},
        "read_percent": 0.0,
    }
    for status in ALL_STATUSES:
        count = count_books_by_status(books, status)
        stats["by_status"][status] = count
    if total > 0:
        read_count = stats["by_status"][STATUS_READ]
        stats["read_percent"] = (read_count / total) * 100
    return stats