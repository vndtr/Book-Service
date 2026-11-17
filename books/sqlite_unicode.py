"""Регистронезависимый LIKE для кириллицы в SQLite.

Встроенный LIKE в SQLite игнорирует регистр только для латиницы, поэтому
lookup icontains и iexact не находили бы «толстой» по запросу «Толстой».
Функция like() переопределяется на версию, учитывающую Unicode.
"""

import re

from django.db.backends.signals import connection_created


def unicode_like(pattern, value, escape=None):
    """Реализация LIKE: % - любая подстрока, _ - один символ."""
    if pattern is None or value is None:
        return None
    pattern = str(pattern)
    parts = []
    i = 0
    while i < len(pattern):
        char = pattern[i]
        if escape and char == escape and i + 1 < len(pattern):
            i += 1
            parts.append(re.escape(pattern[i]))
        elif char == "%":
            parts.append(".*")
        elif char == "_":
            parts.append(".")
        else:
            parts.append(re.escape(char))
        i += 1
    flags = re.IGNORECASE | re.DOTALL
    return re.fullmatch("".join(parts), str(value), flags) is not None


def register_unicode_like(sender, connection, **kwargs):
    """Подключить функцию like() к каждому новому соединению SQLite."""
    if connection.vendor != "sqlite":
        return
    raw = connection.connection
    raw.create_function("like", 2, unicode_like, deterministic=True)
    raw.create_function("like", 3, unicode_like, deterministic=True)


def connect():
    """Подписаться на сигнал создания соединения с базой данных."""
    connection_created.connect(
        register_unicode_like,
        dispatch_uid="books_unicode_like",
    )
