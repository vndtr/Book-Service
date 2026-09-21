
from enum import Enum


class Status(str, Enum):
    """Перечисление статусов чтения книги.
    Наследуется от str, чтобы объекты можно было использовать
    как обычные строки (для JSON и сравнения).
    """

    WANT_TO_READ = "хочу прочитать"
    READING = "читаю"
    READ = "прочитано"
    ON_HOLD = "отложено"

    def display_name(self) -> str:
        """Вернуть читаемое название статуса."""
        return STATUS_DISPLAY[self.value]

    def is_read(self) -> bool:
        """Проверить, означает ли статус прочитанную книгу."""
        return self == Status.READ

    @classmethod
    def from_string(cls, value: str) -> "Status":
        """Создать статус из строки. Вернуть WANT_TO_READ при ошибке."""
        for status in cls:
            if status.value == value:
                return status
        return cls.WANT_TO_READ

    @classmethod
    def all_values(cls) -> list:
        """Вернуть список всех значений статусов."""
        return [status.value for status in cls]


# Соответствие значений статусов и их отображаемых названий
STATUS_DISPLAY = {
    Status.WANT_TO_READ.value: "Хочу прочитать",
    Status.READING.value: "Читаю",
    Status.READ.value: "Прочитано",
    Status.ON_HOLD.value: "Отложено",
}

# Константы для удобства использования в коде
STATUS_WANT_TO_READ = Status.WANT_TO_READ.value
STATUS_READING = Status.READING.value
STATUS_READ = Status.READ.value
STATUS_ON_HOLD = Status.ON_HOLD.value

ALL_STATUSES = Status.all_values()


def get_status_display(status: str) -> str:
    """Вернуть читаемое название статуса по строке."""
    return STATUS_DISPLAY.get(status, "Неизвестный статус")


def is_valid_status(status: str) -> bool:
    """Проверить, что строка — допустимый статус."""
    return status in ALL_STATUSES


def is_read_status(status: str) -> bool:
    """Проверить, что строка означает прочитанную книгу."""
    return status == STATUS_READ
