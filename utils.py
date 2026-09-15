"""Вспомогательные функции проекта."""

from datetime import date, datetime
from typing import Optional


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число с проверкой."""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Ошибка: введите целое число.")


def input_non_empty(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: значение не может быть пустым.")


def input_date(prompt: str) -> date:
    """Запросить дату в формате ДД.ММ.ГГГГ."""
    while True:
        value = input(prompt).strip()
        try:
            return datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: неверный формат даты. Используйте ДД.ММ.ГГГГ.")


def input_status(prompt: str, statuses: list[str]) -> str:
    """Запросить статус из списка доступных."""
    print("Доступные статусы:")
    for i, status in enumerate(statuses, 1):
        print(f"  {i}. {status}")
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(statuses):
                return statuses[choice - 1]
            print(f"Ошибка: введите число от 1 до {len(statuses)}.")
        except ValueError:
            print("Ошибка: введите число.")