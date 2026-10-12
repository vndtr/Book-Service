from html import escape

from django.http import HttpResponse

from homepage.views import page
from models import BookList
from models.status import (
    STATUS_ON_HOLD,
    STATUS_READ,
    STATUS_READING,
    STATUS_WANT_TO_READ,
    get_status_display,
)
from storage import load_books

# Цвет бейджа Bootstrap для каждого статуса чтения
STATUS_BADGES = {
    STATUS_READ: "bg-success",
    STATUS_READING: "bg-primary",
    STATUS_WANT_TO_READ: "bg-info text-dark",
    STATUS_ON_HOLD: "bg-secondary",
}


def load_book_list():
    """Загрузить книги из data/books.json в объект BookList (ПР3)."""
    book_list = BookList()
    for book in load_books():
        book_list.add(book)
    return book_list


def books(request):
    """Страница /books/: список книг из data/books.json."""
    book_list = load_book_list()
    items = ""
    for book in book_list:
        status = get_status_display(book.status)
        badge = STATUS_BADGES.get(book.status, "bg-secondary")
        title = escape(book.title)
        author = escape(book.author)
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/books/{book.id}/">{title} – {author}</a>
            <span class="badge {badge}">{status}</span>
        </li>
        """
    if not items:
        items = '<li class="list-group-item">Список книг пуст.</li>'
    content = f"""
    <h1>Книги</h1>
    <p>Всего книг: {len(book_list)}</p>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Book Service – книги", content))


def book_detail(request, book_id):
    """Страница /books/<id>/: информация об отдельной книге."""
    book = load_book_list().find_by_id(book_id)
    if book is None:
        content = """
        <h1 class="text-danger">Книга не найдена</h1>
        <a href="/books/" class="btn btn-outline-secondary">
            ← к списку книг
        </a>
        """
        return HttpResponse(
            page("Книга не найдена", content),
            status=404,
        )

    status = get_status_display(book.status)
    badge = STATUS_BADGES.get(book.status, "bg-secondary")
    is_read = "да" if book.is_read() else "нет"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{escape(book.title)}</h5>
            <p class="card-text">
                <strong>ID:</strong> {book.id}
            </p>
            <p class="card-text">
                <strong>Автор:</strong> {escape(book.author)}
            </p>
            <p class="card-text">
                <strong>Год издания:</strong> {book.year}
            </p>
            <p class="card-text">
                <strong>Дата добавления:</strong>
                {escape(book.date_added)}
            </p>
            <p class="card-text">
                Статус:
                <span class="badge {badge}">{status}</span>
            </p>
            <p class="card-text">
                <strong>Прочитана:</strong> {is_read}
            </p>
            <a href="/books/" class="btn btn-outline-secondary">
                ← к списку книг
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(escape(book.title), content),
        status=200,
    )
