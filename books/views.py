from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Min, Max, Q
from .models import Book

STATUS_BADGES = {
    "прочитано": "bg-success",
    "читаю": "bg-primary",
    "хочу прочитать": "bg-info text-dark",
    "отложено": "bg-secondary",
}


def books(request):
    """Страница /books/: список книг, фильтры по статусу и годам."""
    books_qs = Book.objects.select_related('user').all()

    status = request.GET.get("status", "").strip()
    year_from = request.GET.get("year_from", "").strip()
    year_to = request.GET.get("year_to", "").strip()

    if status:
        books_qs = books_qs.filter(status=status)

    if year_from.isdigit():
        books_qs = books_qs.filter(year__gte=int(year_from))
    if year_to.isdigit():
        books_qs = books_qs.filter(year__lte=int(year_to))

    books_qs = books_qs.order_by('title')

    paginator = Paginator(books_qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    books_list = []
    for b in page_obj:
        books_list.append({
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "year": b.year,
            "status": b.status,
            "user_name": b.user.name,
            "badge_class": STATUS_BADGES.get(b.status, "bg-secondary"),
            "status_display": b.get_status_display(),
        })

    context = {
        "books": books_list,
        "page_obj": page_obj,
        "status": status,
        "year_from": year_from,
        "year_to": year_to,
    }
    return render(request, "books/book_list.html", context)


def book_detail(request, book_id):
    """Страница /books/<id>/: информация об отдельной книге."""
    book = get_object_or_404(Book.objects.select_related('user'), pk=book_id)

    context = {
        "book": book,
        "badge_class": STATUS_BADGES.get(book.status, "bg-secondary"),
        "status_display": book.get_status_display(),
        "is_read": book.status == "прочитано",
    }
    return render(request, "books/book_detail.html", context)


def stats(request):
    """Страница /books/stats/: статистика (GROUP BY, COUNT, AVG)."""
    by_status = Book.objects.values('status').annotate(count=Count('id'))

    years = Book.objects.aggregate(
        min_year=Min('year'),
        max_year=Max('year'),
        avg_year=Avg('year')
    )

    by_user = Book.objects.values('user__name').annotate(
        books_count=Count('id')
    ).order_by('-books_count')

    total = Book.objects.count()
    newest = Book.objects.order_by('-year')[:3]

    active_readers = Book.objects.values('user__name').annotate(
        books_count=Count('id')
    ).filter(books_count__gte=5)

    context = {
        "by_status": by_status,
        "years": years,
        "by_user": by_user,
        "total": total,
        "newest": newest,
        "active_readers": active_readers,
    }
    return render(request, "books/stats.html", context)


def search_books(request):
    """Страница /books/search/: поиск книг по автору или названию."""
    query = request.GET.get("q", "").strip()
    results = Book.objects.none()
    if query:
        results = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

    context = {
        "query": query,
        "results": results,
    }
    return render(request, "books/search.html", context)


def change_status(request, book_id):
    """Изменение статуса книги (POST-запрос)."""
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Book.STATUS_CHOICES):
            book = get_object_or_404(Book, pk=book_id)
            book.status = new_status
            book.save(update_fields=['status'])
    return redirect("books:detail", book_id=book_id)
