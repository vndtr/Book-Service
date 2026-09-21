"""Тесты сущности "Книга"."""

from book import (
    create_book,
    get_book_author,
    get_book_info,
    get_book_status,
    get_book_title,
    get_book_year,
    matches_query,
    set_book_status,
    validate_book,
)
from status import STATUS_READ, STATUS_READING, STATUS_WANT_TO_READ


def test_create_book():
    """Создание книги."""
    book = create_book(1, "Война и мир", "Толстой", 1869, STATUS_WANT_TO_READ)
    assert book["id"] == 1
    assert book["title"] == "Война и мир"
    assert book["status"] == STATUS_WANT_TO_READ


def test_get_book_title():
    """Получение названия."""
    book = create_book(1, "Война и мир", "Толстой", 1869, STATUS_WANT_TO_READ)
    assert get_book_title(book) == "Война и мир"


def test_get_book_author():
    """Получение автора."""
    book = create_book(1, "Книга", "Автор", 2000, STATUS_READ)
    assert get_book_author(book) == "Автор"


def test_get_book_year():
    """Получение года."""
    book = create_book(1, "Книга", "Автор", 2000, STATUS_READ)
    assert get_book_year(book) == 2000


def test_get_book_status():
    """Получение статуса."""
    book = create_book(1, "Книга", "Автор", 2000, STATUS_READING)
    assert get_book_status(book) == STATUS_READING


def test_set_book_status():
    """Установка нового статуса."""
    book = create_book(1, "Книга", "Автор", 2000, STATUS_WANT_TO_READ)
    result = set_book_status(book, STATUS_READING)
    assert result is True
    assert book["status"] == STATUS_READING


def test_set_book_status_invalid():
    """Установка некорректного статуса."""
    book = create_book(1, "Книга", "Автор", 2000, STATUS_WANT_TO_READ)
    result = set_book_status(book, "неверный")
    assert result is False
    assert book["status"] == STATUS_WANT_TO_READ


def test_matches_query_title():
    """Поиск по названию."""
    book = create_book(1, "Война и мир", "Толстой", 1869, STATUS_READ)
    assert matches_query(book, "война") is True
    assert matches_query(book, "ВОЙНА") is True


def test_matches_query_author():
    """Поиск по автору."""
    book = create_book(1, "Война и мир", "Толстой", 1869, STATUS_READ)
    assert matches_query(book, "толстой") is True


def test_matches_query_no_match():
    """Нет совпадений."""
    book = create_book(1, "Война и мир", "Толстой", 1869, STATUS_READ)
    assert matches_query(book, "пушкин") is False


def test_validate_book_ok():
    """Корректные данные."""
    assert validate_book("Книга", "Автор", 2000) is None


def test_validate_book_empty_title():
    """Пустое название."""
    assert validate_book("", "Автор", 2000) == "Название не может быть пустым"


def test_validate_book_empty_author():
    """Пустой автор."""
    result = validate_book("Книга", "", 2000)
    assert result == "Автор не может быть пустым"


def test_validate_book_bad_year():
    """Некорректный год."""
    assert validate_book("Книга", "Автор", -5) == "Некорректный год издания"
    assert validate_book("Книга", "Автор", 3000) == "Некорректный год издания"


def test_get_book_info():
    """Формат строки с информацией."""
    book = create_book(1, "Книга", "Автор", 2000, STATUS_READ)
    info = get_book_info(book)
    assert "[1]" in info
    assert "Книга" in info
    assert "Прочитано" in info
