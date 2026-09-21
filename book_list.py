
from typing import Optional
from book import (
    create_book,
    get_book_info,
    get_book_status,
    get_book_title,
    get_book_year,
    matches_query,
    set_book_status,
)
from status import (
    ALL_STATUSES,
    STATUS_READ,
    get_status_display,
)


def add_book(
    books: list,
    title: str,
    author: str,
    year: int,
    status: str,
    date_added: str = "",
) -> dict:
    """Добавить книгу в список и вернуть её словарь."""
    book_id = len(books) + 1
    book = create_book(book_id, title, author, year, status, date_added)
    books.append(book)
    return book


def find_book_by_id(books: list, book_id: int) -> Optional[dict]:
    """Найти книгу по идентификатору."""
    for book in books:
        if book["id"] == book_id:
            return book
    return None


def find_books(books: list, query: str) -> list:
    """Найти книги по подстроке в названии или авторе."""
    return [book for book in books if matches_query(book, query)]


def filter_books_by_status(books: list, status: str) -> list:
    """Отобрать книги по статусу."""
    return [book for book in books if get_book_status(book) == status]


def count_books_by_status(books: list, status: str) -> int:
    """Подсчитать количество книг с заданным статусом."""
    return sum(1 for book in books if get_book_status(book) == status)


def sort_books_by_title(books: list) -> list:
    """Отсортировать книги по названию."""
    return sorted(books, key=lambda book: get_book_title(book).lower())


def sort_books_by_year(books: list) -> list:
    """Отсортировать книги по году издания."""
    return sorted(books, key=lambda book: get_book_year(book))


def change_status(books: list, book_id: int, new_status: str) -> bool:
    """Изменить статус книги. Вернуть True при успехе."""
    book = find_book_by_id(books, book_id)
    if book is None:
        return False
    return set_book_status(book, new_status)


def remove_book(books: list, book_id: int) -> Optional[dict]:
    """Удалить книгу. Вернуть удалённую книгу или None."""
    for i, book in enumerate(books):
        if book["id"] == book_id:
            return books.pop(i)
    return None


def get_statistics(books: list) -> dict:
    """Вернуть статистику по списку книг."""
    total = len(books)
    by_status: dict = {}
    for status in ALL_STATUSES:
        by_status[status] = count_books_by_status(books, status)

    read_percent = 0.0
    if total > 0:
        read_count = by_status[STATUS_READ]
        read_percent = (read_count / total) * 100

    return {
        "total": total,
        "by_status": by_status,
        "read_percent": read_percent,
    }


def get_all_book_info(books: list) -> list:
    """Вернуть список строк с информацией о всех книгах."""
    return [get_book_info(book) for book in books]


def get_status_summary(books: list) -> dict:
    """Вернуть сводку: отображаемое имя статуса → количество."""
    result: dict = {}
    for status in ALL_STATUSES:
        count = count_books_by_status(books, status)
        result[get_status_display(status)] = count
    return result
