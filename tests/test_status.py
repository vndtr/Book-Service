from models.status import (
    ALL_STATUSES,
    STATUS_ON_HOLD,
    STATUS_READ,
    STATUS_READING,
    STATUS_WANT_TO_READ,
    Status,
    get_status_display,
    is_read_status,
    is_valid_status,
)


def test_all_statuses_count():
    """Всего должно быть 4 статуса."""
    assert len(ALL_STATUSES) == 4


def test_status_display_name():
    """Отображаемое имя статуса."""
    assert Status.READ.display_name() == "Прочитано"
    assert Status.READING.display_name() == "Читаю"


def test_get_status_display_read():
    """Отображение статуса 'прочитано'."""
    assert Status.READ.value == "прочитано"


def test_get_status_display_unknown():
    """Неизвестный статус."""
    assert get_status_display("нечто") == "Неизвестный статус"


def test_status_all_values():
    """Список всех значений."""
    values = Status.all_values()
    assert "прочитано" in values
    assert "читаю" in values


def test_status_from_string():
    """Создание статуса из строки."""
    assert Status.from_string("прочитано") == Status.READ
    assert Status.from_string("читаю") == Status.READING


def test_status_from_string_invalid():
    """Неизвестная строка даёт WANT_TO_READ."""
    assert Status.from_string("ерунда") == Status.WANT_TO_READ


def test_get_status_display():
    """Функция отображения."""
    assert get_status_display(STATUS_READ) == "Прочитано"


def test_is_valid_status():
    """Валидация статуса."""
    assert is_valid_status(STATUS_READING) is True
    assert is_valid_status("неверный") is False


def test_is_read_status():
    """Проверка прочитанности."""
    assert is_read_status(STATUS_READ) is True
    assert is_read_status(STATUS_READING) is False


def test_status_constants():
    """Константы соответствуют значениям."""
    assert STATUS_READ == "прочитано"
    assert STATUS_READING == "читаю"
    assert STATUS_WANT_TO_READ == "хочу прочитать"
    assert STATUS_ON_HOLD == "отложено"
