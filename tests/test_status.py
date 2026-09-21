"""Тесты сущности "Статус"."""

from status import (
    ALL_STATUSES,
    STATUS_ON_HOLD,
    STATUS_READ,
    STATUS_READING,
    STATUS_WANT_TO_READ,
    get_status_display,
    is_read_status,
    is_valid_status,
)


def test_all_statuses_count():
    """Всего должно быть 4 статуса."""
    assert len(ALL_STATUSES) == 4


def test_get_status_display_read():
    """Отображение статуса 'прочитано'."""
    assert get_status_display(STATUS_READ) == "Прочитано"


def test_get_status_display_unknown():
    """Неизвестный статус."""
    assert get_status_display("что-то") == "Неизвестный статус"


def test_is_valid_status_true():
    """Допустимые статусы."""
    assert is_valid_status(STATUS_READING) is True
    assert is_valid_status(STATUS_WANT_TO_READ) is True
    assert is_valid_status(STATUS_ON_HOLD) is True


def test_is_valid_status_false():
    """Недопустимый статус."""
    assert is_valid_status("прочитал") is False


def test_is_read_status():
    """Проверка статуса 'прочитано'."""
    assert is_read_status(STATUS_READ) is True
    assert is_read_status(STATUS_READING) is False
