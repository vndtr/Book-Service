
STATUS_WANT_TO_READ = "хочу прочитать"
STATUS_READING = "читаю"
STATUS_READ = "прочитано"
STATUS_ON_HOLD = "отложено"

ALL_STATUSES = [
    STATUS_WANT_TO_READ,
    STATUS_READING,
    STATUS_READ,
    STATUS_ON_HOLD,
]

# Соответствие статусов и их отображаемых названий
STATUS_DISPLAY = {
    STATUS_WANT_TO_READ: "Хочу прочитать",
    STATUS_READING: "Читаю",
    STATUS_READ: "Прочитано",
    STATUS_ON_HOLD: "Отложено",
}


def get_status_display(status: str) -> str:
    """Вернуть читаемое название статуса."""
    return STATUS_DISPLAY.get(status, "Неизвестный статус")


def is_valid_status(status: str) -> bool:
    """Проверить, что статус входит в список допустимых."""
    return status in ALL_STATUSES


def is_read_status(status: str) -> bool:
    """Проверить, что статус означает прочитанную книгу."""
    return status == STATUS_READ
