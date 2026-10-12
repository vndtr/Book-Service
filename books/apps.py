"""Конфигурация приложения books."""

from django.apps import AppConfig


class BooksConfig(AppConfig):
    """Настройки Django-приложения books."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "books"
