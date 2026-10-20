import sqlite3
from html import escape
from django.shortcuts import render

from models.status import get_status_display

DB_PATH = "data/library.sqlite"

STATUS_BADGES = {
    "прочитано": "bg-success",
    "читаю": "bg-primary",
    "хочу прочитать": "bg-info text-dark",
    "отложено": "bg-secondary",
}


def get_db_connection():
    """Создание подключения к БД."""
    conn = sqlite3.connect(DB_PATH)
    # Позволяет обращаться к полям по именам: row['title']
    conn.row_factory = sqlite3.Row
    return conn


def books(request):
    """Страница /books/: список книг из базы данных."""
    conn = get_db_connection()
    books_data = conn.execute("""
        SELECT books.id, books.title, books.author, books.year, 
               books.status, users.name AS user_name
        FROM books
        JOIN users ON books.user_id = users.id
        ORDER BY books.title;
    """).fetchall()
    conn.close()

    books_list = []
    for b in books_data:
        books_list.append({
            "id": b["id"],
            "title": b["title"],
            "author": b["author"],
            "year": b["year"],
            "status": b["status"],
            "user_name": b["user_name"],
            "badge_class": STATUS_BADGES.get(b["status"], "bg-secondary"),
            "status_display": get_status_display(b["status"]),
        })

    context = {"books": books_list}
    return render(request, "books/book_list.html", context)


def book_detail(request, book_id):
    """Страница /books/<id>/: информация об отдельной книге."""
    conn = get_db_connection()
    book = conn.execute("""
        SELECT books.*, users.name AS user_name
        FROM books
        JOIN users ON books.user_id = users.id
        WHERE books.id = ?
    """, (book_id,)).fetchone()
    conn.close()

    if book is None:
        return render(request, "books/book_detail.html", {"book": None}, status=404)

    context = {
        "book": book,
        "badge_class": STATUS_BADGES.get(book["status"], "bg-secondary"),
        "status_display": get_status_display(book["status"]),
        "is_read": book["status"] == "прочитано",
    }
    return render(request, "books/book_detail.html", context, status=200)


def stats(request):
    """Страница /books/stats/: статистика (GROUP BY, COUNT)."""
    conn = get_db_connection()
    by_status = conn.execute("""
        SELECT status, COUNT(*) AS count
        FROM books
        GROUP BY status;
    """).fetchall()
    years = conn.execute("""
        SELECT MIN(year) AS min_year, MAX(year) AS max_year FROM books;
    """).fetchone()
    conn.close()

    context = {
        "by_status": by_status,
        "years": years,
    }
    return render(request, "books/stats.html", context)


def search_books(request):
    """Страница /books/search/: поиск книг по автору или названию."""
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        conn = get_db_connection()
        results = conn.execute("""
            SELECT title, author, year
            FROM books
            WHERE author LIKE ? OR title LIKE ?
        """, (f"%{query}%", f"%{query}%")).fetchall()
        conn.close()

    context = {
        "query": query,
        "results": results,
    }
    return render(request, "books/search.html", context)

def change_status(request, book_id):
    """Изменение статуса книги (POST-запрос)."""
    if request.method == "POST":
        new_status = request.POST.get("status")
        conn = get_db_connection()
        # Запрос UPDATE для обновления данных в БД
        conn.execute("""
            UPDATE books 
            SET status = ? 
            WHERE id = ?
        """, (new_status, book_id))
        conn.commit()  # Сохраняем изменения
        conn.close()
        
    # Перенаправляем обратно на страницу книги
    from django.shortcuts import redirect
    return redirect("books:detail", book_id=book_id)