from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, Min, Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from users.models import User
from .models import Book

STATUS_BADGES = {
    Book.Status.READ: "bg-success",
    Book.Status.READING: "bg-primary",
    Book.Status.WANT_TO_READ: "bg-info text-dark",
    Book.Status.ON_HOLD: "bg-secondary",
}

SORT_FIELDS = {
    "title": "title",
    "author": "author",
    "year": "year",
    "year_desc": "-year",
    "user": "user__name",
}

PAGE_SIZE = 5


def books(request):
    """Страница /books/: список книг, фильтры по статусу и годам."""
    books_qs = Book.objects.active().select_related("user")

    status = request.GET.get("status", "").strip()
    year_from = request.GET.get("year_from", "").strip()
    year_to = request.GET.get("year_to", "").strip()

    if status:
        books_qs = books_qs.filter(status=status)
    if year_from.isdigit():
        books_qs = books_qs.filter(year__gte=int(year_from))
    if year_to.isdigit():
        books_qs = books_qs.filter(year__lte=int(year_to))

    sort = request.GET.get("sort", "title")
    sort_field = SORT_FIELDS.get(sort, "title")
    books_qs = books_qs.order_by(sort_field)

    paginator = Paginator(books_qs, PAGE_SIZE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "books": page_obj,
        "page_obj": page_obj,
        "total": paginator.count,
        "status": status,
        "year_from": year_from,
        "year_to": year_to,
        "sort": sort,
        "statuses": Book.Status.choices,
    }
    return render(
        request, "books/book_list.html", context
    )


def book_detail(request, slug):
    """Страница /books/<slug>/: информация об отдельной книге."""
    book = get_object_or_404(Book.objects.select_related("user"), slug=slug)

    context = {
        "book": book,
        "badge_class": STATUS_BADGES.get(book.status, "bg-secondary"),
        "status_display": book.get_status_display(),
        "is_read": book.is_read,
        "statuses": Book.Status.choices,
    }
    return render(request, "books/book_detail.html", context)


def book_create(request):
    """Заглушка для создания книги (формы будут в ПР11)."""
    from django.http import HttpResponse

    return HttpResponse("Добавление книг будет реализовано в ПР11.")


def book_update(request, book_id):
    """Заглушка для редактирования (формы будут в ПР11)."""
    from django.http import HttpResponse

    return HttpResponse("Редактирование книг будет реализовано в ПР11.")


@require_POST
def book_hold(request, book_id):
    """Отложить книгу."""
    book = get_object_or_404(Book.objects.active(), pk=book_id)
    book.put_on_hold()
    return redirect("books:list")


@require_POST
def change_status(request, book_id):
    """Изменение статуса книги (только POST-запрос)."""
    new_status = request.POST.get("status")
    book = get_object_or_404(Book, pk=book_id)
    if new_status in Book.Status.values:
        book.status = new_status
        book.save(update_fields=["status"])
    return redirect(book)


def stats(request):
    """Страница /books/stats/: статистика."""
    counts = Book.objects.aggregate(
        total=Count("id"),
        want_to_read=Count(
            "id", filter=Q(status=Book.Status.WANT_TO_READ)
        ),
        reading=Count("id", filter=Q(status=Book.Status.READING)),
        read=Count("id", filter=Q(status=Book.Status.READ)),
        on_hold=Count("id", filter=Q(status=Book.Status.ON_HOLD)),
    )
    labels = dict(Book.Status.choices)
    by_status = [
        {
            "label": labels.get(row["status"], row["status"]),
            "count": row["count"],
        }
        for row in (
            Book.objects.values("status")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
    ]
    years = Book.objects.aggregate(
        min_year=Min("year"),
        max_year=Max("year"),
        avg_year=Avg("year"),
    )
    by_user = (
        User.objects.annotate(books_count=Count("books"))
        .values("name", "books_count")
        .order_by("-books_count")
    )
    active_readers = (
        User.objects.annotate(books_count=Count("books"))
        .filter(books_count__gte=5)
        .values("name", "books_count")
    )

    context = {
        "counts": counts,
        "by_status": by_status,
        "years": years,
        "by_user": by_user,
        "newest": Book.objects.order_by("-year")[:3],
        "active_readers": active_readers,
    }
    return render(request, "books/stats.html", context)


def search_books(request):
    """Страница /books/search/: поиск."""
    query = request.GET.get("q", "").strip()
    results = Book.objects.none()
    if query:
        query_lower = query.lower()
        results = (
            Book.objects.select_related("user")
            .annotate(
                lower_title=Lower("title"),
                lower_author=Lower("author"),
                lower_user=Lower("user__name"),
            )
            .filter(
                Q(lower_title__contains=query_lower)
                | Q(lower_author__contains=query_lower)
                | Q(lower_user__contains=query_lower)
            )
            .order_by("title")
        )
    return render(
        request,
        "books/search.html",
        {"query": query, "results": results},
    )
