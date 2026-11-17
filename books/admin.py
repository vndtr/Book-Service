"""Настройка панели администрирования приложения books."""
from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        "id", "title", "author", "year", "status",
        "user", "is_classic_display"  # Выводим вычисляемое поле
    )
    list_display_links = ("id", "title")
    search_fields = ("title", "author", "user__name")
    list_filter = ("status", "is_classic", "year", "user")
    ordering = ("title",)
    list_per_page = 20
    list_editable = ("status",)

    # 1. Устраняем N+1 (JOIN пользователя)
    list_select_related = ("user",)

    # 2. Кнопка "Посмотреть на сайте"
    view_on_site = True

    # 3. Массовые действия
    actions = ["mark_as_read", "mark_as_on_hold"]

    @admin.display(boolean=True, description="Классика")
    def is_classic_display(self, obj):
        return obj.is_classic

    @admin.action(description="Отметить как прочитанные")
    def mark_as_read(self, request, queryset):
        queryset.update(status=Book.Status.READ)
        self.message_user(request, "Выбранные книги отмечены как прочитанные.")

    @admin.action(description="Отложить выбранные книги")
    def mark_as_on_hold(self, request, queryset):
        queryset.update(status=Book.Status.ON_HOLD)
        self.message_user(request, "Выбранные книги отложены.")
