"""Настройка панели администрирования приложения books."""

from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Настройки отображения книг в админ-панели."""

    list_display = (
        "id",
        "title",
        "author",
        "year",
        "status",
        "date_added",
        "user",
        "is_read_display",
    )
    list_display_links = ("id", "title")
    search_fields = ("title", "author", "user__name")
    list_filter = ("status", "year", "user")
    ordering = ("title",)
    list_per_page = 20
    list_editable = ("status",)
    fieldsets = (
        ("Основное", {
            "fields": ("title", "author", "year", "status")
        }),
        ("Служебное", {
            "fields": ("date_added", "user"),
        }),
    )

    @admin.display(boolean=True, description="Прочитана")
    def is_read_display(self, obj):
        """Признак «прочитана»."""
        return obj.status == "прочитано"
