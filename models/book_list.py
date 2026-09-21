from typing import List, Optional

from models.book import Book
from models.status import (
    ALL_STATUSES,
    get_status_display,
)
from models.status import Status


class BookList:
    """Список книг пользователя."""

    def __init__(self, user_name: str = "Пользователь") -> None:
        """Создать пустой список книг."""
        self.user_name: str = user_name
        self.books: List[Book] = []

    def add(self, book: Book) -> Book:
        """Добавить книгу в список."""
        if book.id == 0:
            book.id = len(self.books) + 1
        self.books.append(book)
        return book

    def find_by_id(self, book_id: int) -> Optional[Book]:
        """Найти книгу по идентификатору."""
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def find(self, query: str) -> List[Book]:
        """Найти книги по подстроке в названии или авторе."""
        return [book for book in self.books if book.matches_query(query)]

    def filter_by_status(self, status: str) -> List[Book]:
        """Отобрать книги по статусу."""
        return [book for book in self.books if book.status == status]

    def count_by_status(self, status: str) -> int:
        """Подсчитать книги с заданным статусом."""
        return sum(1 for book in self.books if book.status == status)

    def sort_by_title(self) -> List[Book]:
        """Отсортировать книги по названию."""
        return sorted(self.books, key=lambda book: book.title.lower())

    def sort_by_year(self) -> List[Book]:
        """Отсортировать книги по году издания."""
        return sorted(self.books, key=lambda book: book.year)

    def change_status(self, book_id: int, new_status: str) -> bool:
        """Изменить статус книги."""
        book = self.find_by_id(book_id)
        if book is None:
            return False
        return book.set_status(new_status)

    def remove(self, book_id: int) -> Optional[Book]:
        """Удалить книгу по идентификатору."""
        for i, book in enumerate(self.books):
            if book.id == book_id:
                return self.books.pop(i)
        return None

    def get_statistics(self) -> dict:
        """Вернуть статистику по списку книг."""
        total = len(self.books)
        by_status: dict = {}
        by_status = {
            status.value: self.count_by_status(status.value)
            for status in Status
        }

        read_percent = 0.0
        if total > 0:
            read_count = by_status[Status.READ.value]
            read_percent = (read_count / total) * 100

        return {
            "total": total,
            "by_status": by_status,
            "read_percent": read_percent,
        }

    def get_status_summary(self) -> dict:
        """Сводка: отображаемое имя статуса → количество."""
        return {
            get_status_display(status): self.count_by_status(status)
            for status in ALL_STATUSES
        }

    def __len__(self) -> int:
        """Количество книг в списке."""
        return len(self.books)

    def __iter__(self):
        """Итератор по книгам."""
        return iter(self.books)

    def __str__(self) -> str:
        """Строковое представление списка."""
        return (
            f"Список книг пользователя {self.user_name}: "
            f"{len(self.books)} книг(и)"
        )
