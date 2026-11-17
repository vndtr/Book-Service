"""Настройка панели администрирования приложения users."""

from django.contrib import admin
from django.db.models import Count, Q

from books.models import Book

from .models import User


class BookInline(admin.TabularInline):
    """Встроенный список книг пользователя в карточке пользователя."""

    model = Book
    extra = 0
    can_delete = False
    fields = ("title", "author", "year", "status", "date_added")
    readonly_fields = ("date_added",)
    show_change_link = True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Настройки отображения пользователей в админ-панели."""

    list_display = ("id", "name", "created_at", "active_books_count")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_filter = ("created_at",)
    ordering = ("name",)
    readonly_fields = ("id",)
    inlines = (BookInline,)

    def get_queryset(self, request):
        """Число книг считается аннотацией: один запрос на весь список."""
        queryset = super().get_queryset(request)
        return queryset.annotate(
            active_books=Count(
                "books",
                filter=~Q(books__status=Book.Status.ON_HOLD),
            ),
        )

    @admin.display(description="Активных книг", ordering="active_books")
    def active_books_count(self, obj):
        """Количество книг пользователя, кроме отложенных."""
        return obj.active_books
