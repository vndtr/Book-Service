from django.contrib import admin
from django.db.models import Count

from books.models import Book
from .models import User


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "books_count")
    search_fields = ("name",)
    inlines = [BookInline]

    def get_queryset(self, request):
        """Считаем книги одним SQL-запросом (без N+1)."""
        queryset = super().get_queryset(request)
        return queryset.annotate(_books_count=Count("books"))

    @admin.display(description="Книг", ordering="_books_count")
    def books_count(self, obj):
        return obj._books_count
