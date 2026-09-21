"""Сущность "Книга" — данные одной книги."""

from typing import Optional
from status import (
    is_valid_status,
    get_status_display,
)


def create_book(
    book_id: int,
    title: str,
    author: str,
    year: int,
    status: str,
    date_added: str = "",
) -> dict:
    """Создать словарь книги."""
    return {
        "id": book_id,
        "title": title,
        "author": author,
        "year": year,
        "status": status,
        "date_added": date_added,
    }


def get_book_title(book: dict) -> str:
    """Вернуть название книги."""
    return book.get("title", "")


def get_book_author(book: dict) -> str:
    """Вернуть автора книги."""
    return book.get("author", "")


def get_book_year(book: dict) -> int:
    """Вернуть год издания книги."""
    return book.get("year", 0)


def get_book_status(book: dict) -> str:
    """Вернуть статус книги."""
    return book.get("status", "")


def set_book_status(book: dict, new_status: str) -> bool:
    """Установить новый статус книги. Вернуть True при успехе."""
    if not is_valid_status(new_status):
        return False
    book["status"] = new_status
    return True


def get_book_info(book: dict) -> str:
    """Вернуть строку с информацией о книге."""
    status = get_status_display(get_book_status(book))
    return (
        f"[{book['id']}] \"{get_book_title(book)}\" — "
        f"{get_book_author(book)} ({get_book_year(book)}) | Статус: {status}"
    )


def matches_query(book: dict, query: str) -> bool:
    """Проверить, содержит ли книга подстроку в названии или авторе."""
    query_lower = query.lower()
    title_match = query_lower in get_book_title(book).lower()
    author_match = query_lower in get_book_author(book).lower()
    return title_match or author_match


def validate_book(
    title: str,
    author: str,
    year: int,
) -> Optional[str]:
    """Проверить данные книги. Вернуть текст ошибки или None."""
    if not title.strip():
        return "Название не может быть пустым"
    if not author.strip():
        return "Автор не может быть пустым"
    if year < 0 or year > 2100:
        return "Некорректный год издания"
    return None
