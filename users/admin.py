"""Настройка панели администрирования приложения users."""

from django.contrib import admin

from books.models import Book
from .models import User


class BookInline(admin.TabularInline):
    """Встроенный список книг пользователя в карточке пользователя."""

    model = Book
    extra = 0
    fields = ("title", "author", "year", "status", "date_added")
    readonly_fields = ("date_added",)
    show_change_link = True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Настройки отображения пользователей в админ-панели."""

    list_display = ("id", "name", "created_at", "books_count")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_filter = ("created_at",)
    ordering = ("name",)
    inlines = [BookInline]

    @admin.display(description="Книг")
    def books_count(self, obj):
        """Количество книг у пользователя."""
        return obj.books.count()
