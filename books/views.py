"""Представления приложения books."""

from django.shortcuts import render

from storage import load_books


def books(request):
    """Список всех книг."""
    books_list = load_books("data/books.json")
    context = {"books": books_list}
    return render(request, "books/book_list.html", context)


def book_detail(request, book_id):
    """Страница отдельной книги."""
    books_list = load_books("data/books.json")
    book = None
    for b in books_list:
        if b.id == book_id:
            book = b
            break

    context = {"book": book}
    return render(
        request,
        "books/book_detail.html",
        context,
        status=404 if book is None else 200,
    )


def find_book_by_id(books: list, book_id: int):
    """Найти книгу по идентификатору среди списка Book."""
    for book in books:
        if book.id == book_id:
            return book
    return None
