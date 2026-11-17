"""Настройка панели администрирования приложения books."""

from django.contrib import admin, messages
from django.utils.html import format_html

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
        "user",
        "is_classic",
        "site_link",
    )
    list_display_links = ("id", "title")
    list_editable = ("status",)
    search_fields = ("title", "author", "user__name")
    list_filter = ("status", "is_classic", "year", "user")
    ordering = ("title",)
    list_per_page = 20
    # Связанный пользователь загружается тем же запросом (JOIN).
    list_select_related = ("user",)
    autocomplete_fields = ("user",)
    readonly_fields = ("id", "slug", "is_classic")
    # Ссылка «Посмотреть на сайте» использует get_absolute_url().
    view_on_site = True
    actions = ("put_on_hold_action", "restore_to_plan_action")
    fieldsets = (
        ("Основное", {
            "fields": ("id", "title", "author", "year", "status", "cover"),
        }),
        ("Служебное", {
            "fields": ("slug", "is_classic", "date_added", "user"),
        }),
    )

    @admin.display(description="Страница на сайте")
    def site_link(self, obj):
        """Ссылка на публичную страницу книги."""
        return format_html(
            '<a href="{}" target="_blank">Открыть</a>',
            obj.get_absolute_url(),
        )

    @admin.action(description="Отложить выбранные книги")
    def put_on_hold_action(self, request, queryset):
        """Отложить книги по одной: вызывается метод модели."""
        count = 0
        for book in queryset:
            book.put_on_hold()
            count += 1
        self.message_user(
            request,
            f"Отложено книг: {count}.",
            messages.SUCCESS,
        )

    @admin.action(description="Вернуть в «Хочу прочитать»")
    def restore_to_plan_action(self, request, queryset):
        """Вернуть выбранные книги в список планов одним запросом."""
        updated = queryset.update(status=Book.Status.WANT_TO_READ)
        self.message_user(
            request,
            f"Возвращено книг: {updated}.",
            messages.SUCCESS,
        )
