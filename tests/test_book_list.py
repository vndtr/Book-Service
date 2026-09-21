
from models.book import Book
from models.book_list import BookList
from models.status import (
    STATUS_ON_HOLD,
    STATUS_READ,
    STATUS_READING,
    STATUS_WANT_TO_READ,
)


def make_book(book_id, title, author, year, status):
    """Вспомогательная функция создания книги."""
    return Book(book_id, title, author, year, status)


def test_book_list_creation():
    """Создание списка."""
    bl = BookList("Анна")
    assert bl.user_name == "Анна"
    assert len(bl) == 0


def test_add_book():
    """Добавление книги."""
    bl = BookList()
    book = bl.add(make_book(0, "Книга", "Автор", 2000, STATUS_READ))
    assert len(bl) == 1
    assert book.id == 1


def test_find_book_by_id():
    """Поиск по ID."""
    bl = BookList()
    bl.add(make_book(0, "Книга", "Автор", 2000, STATUS_READ))
    found = bl.find_by_id(1)
    assert found is not None
    assert found.title == "Книга"
    assert bl.find_by_id(99) is None


def test_find_books():
    """Поиск по подстроке."""
    bl = BookList()
    bl.add(make_book(0, "Книга", "Автор", 2000, STATUS_READ))
    found = bl.find_by_id(1)
    assert found is not None
    assert found.title == "Книга"
    assert bl.find_by_id(99) is None


def test_filter_books_by_status():
    """Фильтр по статусу."""
    bl = BookList()
    bl.add(make_book(0, "Книга 1", "Автор", 2000, STATUS_READ))
    bl.add(make_book(0, "Книга 2", "Автор", 2001, STATUS_READING))
    bl.add(make_book(0, "Книга 3", "Автор", 2002, STATUS_READ))
    assert len(bl.filter_by_status(STATUS_READ)) == 2


def test_count_books_by_status():
    """Подсчёт по статусу."""
    bl = BookList()
    bl.add(make_book(0, "Книга 1", "Автор", 2000, STATUS_READ))
    bl.add(make_book(0, "Книга 2", "Автор", 2001, STATUS_READ))
    bl.add(make_book(0, "Книга 3", "Автор", 2002, STATUS_READING))
    assert bl.count_by_status(STATUS_READ) == 2
    assert bl.count_by_status(STATUS_READING) == 1


def test_change_status():
    """Изменение статуса."""
    bl = BookList()
    bl.add(make_book(0, "Книга", "Автор", 2000, STATUS_WANT_TO_READ))
    assert bl.change_status(1, STATUS_READING) is True
    assert bl.find_by_id(1).status == STATUS_READING


def test_change_status_not_found():
    """Изменение статуса несуществующей книги."""
    bl = BookList()
    assert bl.change_status(99, STATUS_READ) is False


def test_remove_book():
    """Удаление книги."""
    bl = BookList()
    bl.add(make_book(0, "Книга", "Автор", 2000, STATUS_READ))
    removed = bl.remove(1)
    assert removed is not None
    assert removed.title == "Книга"
    assert len(bl) == 0


def test_sort_books_by_title():
    """Сортировка по названию."""
    bl = BookList()
    bl.add(make_book(0, "Яблоко", "Автор", 2000, STATUS_READ))
    bl.add(make_book(0, "Апельсин", "Автор", 2001, STATUS_READ))
    sorted_books = bl.sort_by_title()
    assert sorted_books[0].title == "Апельсин"
    assert sorted_books[1].title == "Яблоко"


def test_sort_books_by_year():
    """Сортировка по году."""
    bl = BookList()
    bl.add(make_book(0, "Книга 1", "Автор", 2000, STATUS_READ))
    bl.add(make_book(0, "Книга 2", "Автор", 1990, STATUS_READ))
    sorted_books = bl.sort_by_year()
    assert sorted_books[0].year == 1990


def test_get_statistics_empty():
    """Статистика по пустому списку."""
    bl = BookList()
    stats = bl.get_statistics()
    assert stats["total"] == 0
    assert stats["read_percent"] == 0.0


def test_get_statistics():
    """Статистика."""
    bl = BookList()
    bl.add(make_book(0, "Книга 1", "Автор", 2000, STATUS_READ))
    bl.add(make_book(0, "Книга 2", "Автор", 2001, STATUS_READING))
    stats = bl.get_statistics()
    assert stats["total"] == 2
    assert stats["read_percent"] == 50.0
    assert stats["by_status"][STATUS_READ] == 1


def test_get_status_summary():
    """Сводка по статусам."""
    bl = BookList()
    bl.add(make_book(0, "Книга 1", "Автор", 2000, STATUS_READ))
    bl.add(make_book(0, "Книга 2", "Автор", 2001, STATUS_ON_HOLD))
    summary = bl.get_status_summary()
    assert summary["Прочитано"] == 1
    assert summary["Отложено"] == 1
