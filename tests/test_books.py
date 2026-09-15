"""Тесты функций работы с книгами."""

from books import (
    STATUS_READ,
    STATUS_READING,
    STATUS_WANT_TO_READ,
    add_book,
    count_books_by_status,
    filter_books_by_status,
    find_book_by_id,
    find_books,
    get_statistics,
    remove_book,
    sort_books_by_title,
)


def test_add_book():
    """Тест добавления книги."""
    books = []
    book = add_book(books, "Тест", "Автор", 2020, STATUS_WANT_TO_READ)
    assert len(books) == 1
    assert book["id"] == 1
    assert book["title"] == "Тест"


def test_find_books():
    """Тест поиска книг по подстроке."""
    books = []
    add_book(books, "Война и мир", "Толстой", 1869, STATUS_READ)
    add_book(books, "Мир без конца", "Фоллетт", 2007, STATUS_READING)
    result = find_books(books, "мир")
    assert len(result) == 2


def test_filter_books_by_status():
    """Тест фильтрации по статусу."""
    books = []
    add_book(books, "Книга 1", "Автор 1", 2000, STATUS_READ)
    add_book(books, "Книга 2", "Автор 2", 2001, STATUS_READING)
    add_book(books, "Книга 3", "Автор 3", 2002, STATUS_READ)
    read_books = filter_books_by_status(books, STATUS_READ)
    assert len(read_books) == 2


def test_find_book_by_id():
    """Тест поиска книги по ID."""
    books = []
    add_book(books, "Книга", "Автор", 2020, STATUS_WANT_TO_READ)
    book = find_book_by_id(books, 1)
    assert book is not None
    assert book["title"] == "Книга"
    assert find_book_by_id(books, 99) is None


def test_remove_book():
    """Тест удаления книги."""
    books = []
    add_book(books, "Книга", "Автор", 2020, STATUS_WANT_TO_READ)
    removed = remove_book(books, 1)
    assert removed is not None
    assert removed["title"] == "Книга"
    assert len(books) == 0


def test_count_books_by_status():
    """Тест подсчета книг по статусу."""
    books = []
    add_book(books, "Книга 1", "Автор", 2000, STATUS_READ)
    add_book(books, "Книга 2", "Автор", 2001, STATUS_READ)
    add_book(books, "Книга 3", "Автор", 2002, STATUS_READING)
    assert count_books_by_status(books, STATUS_READ) == 2
    assert count_books_by_status(books, STATUS_READING) == 1


def test_sort_books_by_title():
    """Тест сортировки книг по названию."""
    books = []
    add_book(books, "Яблоко", "Автор", 2000, STATUS_READ)
    add_book(books, "Апельсин", "Автор", 2001, STATUS_READ)
    sorted_books = sort_books_by_title(books)
    assert sorted_books[0]["title"] == "Апельсин"
    assert sorted_books[1]["title"] == "Яблоко"


def test_get_statistics():
    """Тест статистики."""
    books = []
    add_book(books, "Книга 1", "Автор", 2000, STATUS_READ)
    add_book(books, "Книга 2", "Автор", 2001, STATUS_READING)
    stats = get_statistics(books)
    assert stats["total"] == 2
    assert stats["read_percent"] == 50.0
