from django.shortcuts import redirect, render

from db.database import get_connection
from models.status import get_status_display, is_valid_status

STATUS_BADGES = {
    "прочитано": "bg-success",
    "читаю": "bg-primary",
    "хочу прочитать": "bg-info text-dark",
    "отложено": "bg-secondary",
}


def books(request):
    """Страница /books/: список книг, фильтры по статусу и годам."""
    status = request.GET.get("status", "").strip()
    year_from = request.GET.get("year_from", "").strip()
    year_to = request.GET.get("year_to", "").strip()

    sql = """
        SELECT books.id, books.title, books.author, books.year,
               books.status, users.name AS user_name
        FROM books
        JOIN users ON books.user_id = users.id
        WHERE 1 = 1
    """
    params = []
    if status:
        sql += " AND books.status = ?"
        params.append(status)
    if year_from.isdigit():
        sql += " AND books.year >= ?"
        params.append(int(year_from))
    if year_to.isdigit():
        sql += " AND books.year <= ?"
        params.append(int(year_to))
    sql += " ORDER BY books.title;"

    conn = get_connection()
    books_data = conn.execute(sql, params).fetchall()
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

    context = {
    "books": books_list,
    "status": status,
    "year_from": year_from,
    "year_to": year_to,
    }
    return render(request, "books/book_list.html", context)


def book_detail(request, book_id):
    """Страница /books/<id>/: информация об отдельной книге."""
    conn = get_connection()
    book = conn.execute("""
        SELECT books.*, users.name AS user_name
        FROM books
        JOIN users ON books.user_id = users.id
        WHERE books.id = ?
    """, (book_id,)).fetchone()
    conn.close()

    if book is None:
        return render(
            request,
            "books/book_detail.html",
            {"book": None},
            status=404,
        )

    context = {
        "book": book,
        "badge_class": STATUS_BADGES.get(book["status"], "bg-secondary"),
        "status_display": get_status_display(book["status"]),
        "is_read": book["status"] == "прочитано",
    }
    return render(request, "books/book_detail.html", context, status=200)


def stats(request):
    """Страница /books/stats/: статистика (GROUP BY, COUNT, AVG)."""
    conn = get_connection()
    by_status = conn.execute("""
        SELECT status, COUNT(*) AS count
        FROM books
        GROUP BY status;
    """).fetchall()
    years = conn.execute("""
        SELECT MIN(year) AS min_year,
               MAX(year) AS max_year,
               AVG(year) AS avg_year
        FROM books;
    """).fetchone()
    by_user = conn.execute("""
        SELECT users.name AS user_name, COUNT(books.id) AS books_count
        FROM users
        LEFT JOIN books ON users.id = books.user_id
        GROUP BY users.id, users.name
        ORDER BY books_count DESC;
    """).fetchall()
    total = conn.execute(
        "SELECT COUNT(*) AS total FROM books;"
    ).fetchone()
    newest = conn.execute("""
        SELECT title, year FROM books ORDER BY year DESC LIMIT 3;
    """).fetchall()
    active_readers = conn.execute("""
        SELECT users.name AS user_name, COUNT(books.id) AS books_count
        FROM users
        JOIN books ON users.id = books.user_id
        GROUP BY users.id, users.name
        HAVING COUNT(books.id) >= 5;
    """).fetchall()
    conn.close()

    context = {
        "by_status": by_status,
        "years": years,
        "by_user": by_user,
        "total": total["total"],
        "newest": newest,
        "active_readers": active_readers,
    }
    return render(request, "books/stats.html", context)


def search_books(request):
    """Страница /books/search/: поиск книг по автору или названию."""
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        conn = get_connection()
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
        if is_valid_status(new_status):
            conn = get_connection()
            conn.execute("""
                UPDATE books
                SET status = ?
                WHERE id = ?
            """, (new_status, book_id))
            conn.commit()
            conn.close()

    return redirect("books:detail", book_id=book_id)
