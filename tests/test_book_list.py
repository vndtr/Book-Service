
from book_list import (
    add_book,
    change_status,
    count_books_by_status,
    filter_books_by_status,
    find_book_by_id,
    find_books,
    get_statistics,
    get_status_summary,
    remove_book,
    sort_books_by_title,
    sort_books_by_year,
)
from status import (
    STATUS_ON_HOLD,
    STATUS_READ,
    STATUS_READING,
    STATUS_WANT_TO_READ,
)


def test_add_book():
    """Добавление книги."""
    books = []
    book = add_book(books, "Книга", "Автор", 2000, STATUS_WANT_TO_READ)
    assert len(books) == 1
    assert book["id"] == 1


def test_add_multiple_books():
    """Добавление нескольких книг."""
    books = []
    add_book(books, "Книга 1", "Автор 1", 2000, STATUS_READ)
    add_book(books, "Книга 2", "Автор 2", 2001, STATUS_READING)
    assert len(books) == 2
    assert books[1]["id"] == 2


def test_find_book_by_id():
    """Поиск по ID."""
    books = []
    add_book(books, "Книга", "Автор", 2000, STATUS_WANT_TO_READ)
    found = find_book_by_id(books, 1)
    assert found is not None
    assert found["title"] == "Книга"


def test_find_book_by_id_not_found():
    """Книга не найдена."""
    books = []
    assert find_book_by_id(books, 99) is None


def test_find_books():
    """Поиск по подстроке."""
    books = []
    add_book(books, "Война и мир", "Толстой", 1869, STATUS_READ)
    add_book(books, "Мир без конца", "Фоллетт", 2007, STATUS_READING)
    result = find_books(books, "мир")
    assert len(result) == 2


def test_filter_books_by_status():
    """Фильтр по статусу."""
    books = []
    add_book(books, "Книга 1", "Автор", 2000, STATUS_READ)
    add_book(books, "Книга 2", "Автор", 2001, STATUS_READING)
    add_book(books, "Книга 3", "Автор", 2002, STATUS_READ)
    read_books = filter_books_by_status(books, STATUS_READ)
    assert len(read_books) == 2


def test_count_books_by_status():
    """Подсчёт по статусу."""
    books = []
    add_book(books, "Книга 1", "Автор", 2000, STATUS_READ)
    add_book(books, "Книга 2", "Автор", 2001, STATUS_READ)
    add_book(books, "Книга 3", "Автор", 2002, STATUS_READING)
    assert count_books_by_status(books, STATUS_READ) == 2
    assert count_books_by_status(books, STATUS_READING) == 1


def test_change_status():
    """Изменение статуса."""
    books = []
    add_book(books, "Книга", "Автор", 2000, STATUS_WANT_TO_READ)
    result = change_status(books, 1, STATUS_READING)
    assert result is True
    assert books[0]["status"] == STATUS_READING


def test_change_status_not_found():
    """Изменение статуса несуществующей книги."""
    books = []
    assert change_status(books, 99, STATUS_READ) is False


def test_remove_book():
    """Удаление книги."""
    books = []
    add_book(books, "Книга", "Автор", 2000, STATUS_WANT_TO_READ)
    removed = remove_book(books, 1)
    assert removed is not None
    assert removed["title"] == "Книга"
    assert len(books) == 0


def test_remove_book_not_found():
    """Удаление несуществующей книги."""
    books = []
    assert remove_book(books, 99) is None


def test_sort_books_by_title():
    """Сортировка по названию."""
    books = []
    add_book(books, "Яблоко", "Автор", 2000, STATUS_READ)
    add_book(books, "Апельсин", "Автор", 2001, STATUS_READ)
    sorted_books = sort_books_by_title(books)
    assert sorted_books[0]["title"] == "Апельсин"
    assert sorted_books[1]["title"] == "Яблоко"


def test_sort_books_by_year():
    """Сортировка по году."""
    books = []
    add_book(books, "Книга 1", "Автор", 2000, STATUS_READ)
    add_book(books, "Книга 2", "Автор", 1990, STATUS_READ)
    sorted_books = sort_books_by_year(books)
    assert sorted_books[0]["year"] == 1990
    assert sorted_books[1]["year"] == 2000


def test_get_statistics_empty():
    """Статистика по пустому списку."""
    stats = get_statistics([])
    assert stats["total"] == 0
    assert stats["read_percent"] == 0.0


def test_get_statistics():
    """Статистика."""
    books = []
    add_book(books, "Книга 1", "Автор", 2000, STATUS_READ)
    add_book(books, "Книга 2", "Автор", 2001, STATUS_READING)
    stats = get_statistics(books)
    assert stats["total"] == 2
    assert stats["read_percent"] == 50.0
    assert stats["by_status"][STATUS_READ] == 1


def test_get_status_summary():
    """Сводка по статусам."""
    books = []
    add_book(books, "Книга 1", "Автор", 2000, STATUS_READ)
    add_book(books, "Книга 2", "Автор", 2001, STATUS_ON_HOLD)
    summary = get_status_summary(books)
    assert summary["Прочитано"] == 1
    assert summary["Отложено"] == 1
