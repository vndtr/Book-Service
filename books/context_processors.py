from .models import Book


def book_context(request):
    """Передает общие данные Book Service во все шаблоны."""
    return {
        "site_name": "Book Service",
        "books_count": Book.objects.count(),
    }
