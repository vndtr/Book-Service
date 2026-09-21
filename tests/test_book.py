
from models.book import Book
from models.status import STATUS_READ, STATUS_READING, STATUS_WANT_TO_READ


def test_create_book():
    """Создание книги."""
    book = Book(1, "Война и мир", "Толстой", 1869, STATUS_WANT_TO_READ)
    assert book.id == 1
    assert book.title == "Война и мир"
    assert book.author == "Толстой"
    assert book.year == 1869
    assert book.status == STATUS_WANT_TO_READ


def test_set_book_status():
    """Установка корректного статуса."""
    book = Book(1, "Книга", "Автор", 2000, STATUS_WANT_TO_READ)
    assert book.set_status(STATUS_READING) is True
    assert book.status == STATUS_READING


def test_set_book_status_invalid():
    """Установка некорректного статуса."""
    book = Book(1, "Книга", "Автор", 2000, STATUS_WANT_TO_READ)
    assert book.set_status("неверный") is False
    assert book.status == STATUS_WANT_TO_READ


def test_matches_query_title():
    """Поиск по названию."""
    book = Book(1, "Война и мир", "Толстой", 1869, STATUS_READ)
    assert book.matches_query("война") is True
    assert book.matches_query("ВОЙНА") is True


def test_matches_query_author():
    """Поиск по автору."""
    book = Book(1, "Война и мир", "Толстой", 1869, STATUS_READ)
    assert book.matches_query("толстой") is True
    assert book.matches_query("пушкин") is False


def test_validate_book_ok():
    """Корректные данные."""
    assert Book.validate("Книга", "Автор", 2000) is None


def test_validate_book_empty_title():
    """Пустое название."""
    assert Book.validate("", "Автор", 2000) == "Название не может быть пустым"


def test_validate_book_empty_author():
    """Пустой автор."""
    result = Book.validate("Книга", "", 2000)
    assert result == "Автор не может быть пустым"


def test_validate_book_bad_year():
    """Некорректный год."""
    assert Book.validate("Книга", "Автор", -5) == "Некорректный год издания"
    assert Book.validate("Книга", "Автор", 3000) == "Некорректный год издания"


def test_get_book_str():
    """Формат строки с информацией."""
    book = Book(1, "Книга", "Автор", 2000, STATUS_READ)
    assert "[1]" in str(book)
    assert "Книга" in str(book)
    assert "Прочитано" in str(book)


def test_book_to_dict():
    """Преобразование в словарь для JSON."""
    book = Book(1, "Книга", "Автор", 2000, STATUS_READ, "01.01.2026")
    data = book.to_dict()
    assert data["id"] == 1
    assert data["title"] == "Книга"
    assert data["status"] == STATUS_READ
    assert data["date_added"] == "01.01.2026"


def test_book_from_dict():
    """Создание объекта из словаря JSON."""
    data = {
        "id": 1,
        "title": "Книга",
        "author": "Автор",
        "year": 2000,
        "status": STATUS_READ,
        "date_added": "01.01.2026",
    }
    book = Book.from_dict(data)
    assert book.id == 1
    assert book.title == "Книга"
    assert book.year == 2000
    assert book.status == STATUS_READ
