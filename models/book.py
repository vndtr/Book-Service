from typing import Optional

from models.status import (
    get_status_display,
    is_valid_status,
)
from models.status import Status


class Book:
    """Книга в списке чтения."""

    def __init__(
        self,
        book_id: int,
        title: str,
        author: str,
        year: int,
        status: str = Status.WANT_TO_READ.value,
        date_added: str = "",
    ) -> None:
        """Создать объект книги."""
        self.id: int = book_id
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status
        self.date_added: str = date_added

    def set_status(self, new_status: str) -> bool:
        """Установить новый статус книги."""
        if not is_valid_status(new_status):
            return False
        self.status = new_status
        return True

    def is_read(self) -> bool:
        """Проверить, прочитана ли книга."""
        return Status.from_string(self.status).is_read()

    def matches_query(self, query: str) -> bool:
        """Проверить, содержит ли книга подстроку в названии или авторе."""
        query_lower = query.lower()
        return (
            query_lower in self.title.lower()
            or query_lower in self.author.lower()
        )

    def to_dict(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
            "date_added": self.date_added,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """Создать объект Book из словаря."""
        return cls(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"],
            date_added=data.get("date_added", ""),
        )

    @staticmethod
    def validate(title: str, author: str, year: int) -> Optional[str]:
        """Проверить данные книги. Вернуть текст ошибки или None."""
        if not title.strip():
            return "Название не может быть пустым"
        if not author.strip():
            return "Автор не может быть пустым"
        if year < 0 or year > 2100:
            return "Некорректный год издания"
        return None

    def __str__(self) -> str:
        """Строковое представление книги."""
        status = get_status_display(self.status)
        return (
            f'[{self.id}] "{self.title}" — {self.author} '
            f'({self.year}) | Статус: {status}'
        )

    def __repr__(self) -> str:
        """Техническое представление книги."""
        return (
            f"Book({self.id}, {self.title!r}, "
            f"{self.author!r}, {self.year}, {self.status!r})"
        )
