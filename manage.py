#!/usr/bin/env python
"""Утилита командной строки Django для административных задач."""
import os
import sys


def main():
    """Запустить административные команды."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book_service.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Проверьте, что Django "
            "установлен и виртуальное окружение активировано."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
