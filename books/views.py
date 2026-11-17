from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Max, Min, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from users.models import User

from .forms import BookFilterForm, BookForm
from .models import Book

STATUS_BADGES = {
    Book.Status.READ: "bg-success",
    Book.Status.READING: "bg-primary",
    Book.Status.WANT_TO_READ: "bg-info text-dark",
    Book.Status.ON_HOLD: "bg-secondary",
}

# Допустимые поля сортировки: пользователь передает короткое значение,
# а в order_by() попадает только поле из этого словаря.
SORT_FIELDS = {
    "title": "title",
    "author": "author",
    "year": "year",
    "year_desc": "-year",
    "user": "user__name",
}

PAGE_SIZE = 5


def books(request):
    """Страница /books/: форма фильтрации, сортировка и пагинация."""
    # Форма получает GET-параметры; без параметров она не связана с данными.
    form = BookFilterForm(request.GET or None)
    form_valid = form.is_bound and form.is_valid()

    status = None
    year_from = None
    year_to = None
    user_id = None
    sort = "title"

    # Проверенные значения берутся из cleaned_data только после is_valid().
    if form_valid:
        status = form.cleaned_data.get("status")
        year_from = form.cleaned_data.get("year_from")
        year_to = form.cleaned_data.get("year_to")
        selected_user = form.cleaned_data.get("user")
        user_id = selected_user.pk if selected_user else None
        sort = form.cleaned_data.get("sort") or "title"

    if form.is_bound and not form_valid:
        error = "Проверьте введённые значения фильтров."
    else:
        error = None

    # Исходная выборка формируется методами пользовательского QuerySet.
    if status == Book.Status.ON_HOLD:
        books_data = Book.objects.on_hold()
    else:
        books_data = Book.objects.active()
        if status:
            books_data = books_data.filter(status=status)

    if year_from:
        books_data = books_data.filter(year__gte=year_from)
    if year_to:
        books_data = books_data.filter(year__lte=year_to)
    if user_id:
        books_data = books_data.filter(user_id=user_id)

    # Добавляем сведения о связанном пользователе.
    books_data = books_data.annotate(user_name=F("user__name"))

    sort_field = SORT_FIELDS.get(sort, "title")
    books_data = books_data.order_by(sort_field, "id")

    books_data = books_data.values(
        "id",
        "slug",
        "title",
        "author",
        "year",
        "status",
        "user_name",
    )

    paginator = Paginator(books_data, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))

    statuses = dict(Book.Status.choices)
    books_list = []
    for item in page_obj:
        books_list.append({
            **item,
            "badge_class": STATUS_BADGES.get(item["status"], "bg-secondary"),
            "status_display": statuses.get(item["status"], item["status"]),
            "can_edit": item["status"] != Book.Status.ON_HOLD,
        })

    context = {
        "books": books_list,
        "page_obj": page_obj,
        "total": paginator.count,
        "form": form,
        "error": error,
        "sort": sort,
    }
    return render(request, "books/book_list.html", context)


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
    """Создание книги: GET показывает форму, POST сохраняет данные."""
    if request.method == "POST":
        # В форму передаются данные запроса и загруженные файлы.
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            author = form.cleaned_data["author"]
            user = form.cleaned_data["user"]
            # Активная книга с тем же названием и автором уже есть?
            is_duplicate = Book.objects.active().filter(
                user=user,
                title__iexact=title,
                author__iexact=author,
            ).exists()
            if is_duplicate:
                form.add_error(
                    None,
                    "У этого пользователя уже есть такая книга в списке.",
                )
            else:
                # Объект создается, но пока не сохраняется: дата добавления
                # устанавливается приложением, а не пользователем.
                book = form.save(commit=False)
                book.date_added = timezone.localdate().strftime("%d.%m.%Y")
                book.save()
                return redirect("books:list")
    else:
        form = BookForm()

    context = {"form": form}
    return render(request, "books/book_form.html", context)


def book_update(request, book_id):
    """Редактирование существующей книги."""
    # Редактировать можно только книги из активного списка.
    book = get_object_or_404(Book.objects.active(), pk=book_id)

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            title = form.cleaned_data["title"]
            author = form.cleaned_data["author"]
            user = form.cleaned_data["user"]
            # Текущая книга исключается из проверки, чтобы не конфликтовать
            # с самой собой.
            is_duplicate = Book.objects.active().filter(
                user=user,
                title__iexact=title,
                author__iexact=author,
            ).exclude(
                pk=book.pk,
            ).exists()
            if is_duplicate:
                form.add_error(
                    None,
                    "У этого пользователя уже есть такая книга в списке.",
                )
            else:
                form.save()
                return redirect(book)
    else:
        form = BookForm(instance=book)

    context = {"form": form, "book": book}
    return render(request, "books/book_form.html", context)


@require_POST
def book_hold(request, book_id):
    """Отложить книгу (аналог отмены): запись остается в базе."""
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
    """Страница /books/stats/: статистика по статусам и пользователям."""
    # Один запрос: общее число книг и число книг для каждого статуса.
    counts = Book.objects.aggregate(
        total=Count("id"),
        want_to_read=Count(
            "id", filter=Q(status=Book.Status.WANT_TO_READ)
        ),
        reading=Count("id", filter=Q(status=Book.Status.READING)),
        read=Count("id", filter=Q(status=Book.Status.READ)),
        on_hold=Count("id", filter=Q(status=Book.Status.ON_HOLD)),
    )

    # Группировка: для каждого статуса считается число книг.
    labels = dict(Book.Status.choices)
    by_status = [
        {"label": labels.get(row["status"], row["status"]),
         "count": row["count"]}
        for row in Book.objects
        .values("status")
        .annotate(count=Count("id"))
        .order_by("-count", "status")
    ]

    years = Book.objects.aggregate(
        min_year=Min("year"),
        max_year=Max("year"),
        avg_year=Avg("year"),
    )

    # Пользователи без книг тоже попадают в результат.
    by_user = (
        User.objects
        .annotate(books_count=Count("books"))
        .values("name", "books_count")
        .order_by("-books_count", "name")
    )

    # Аналог HAVING: пользователи, у которых не менее 5 книг.
    active_readers = (
        User.objects
        .annotate(books_count=Count("books"))
        .filter(books_count__gte=5)
        .values("name", "books_count")
        .order_by("-books_count", "name")
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
    """Страница /books/search/: поиск по названию, автору и пользователю."""
    query = request.GET.get("q", "").strip()
    results = Book.objects.none()
    if query:
        results = (
            Book.objects
            .select_related("user")
            .filter(
                Q(title__icontains=query)
                | Q(author__icontains=query)
                | Q(user__name__icontains=query)
            )
            .order_by("title")
        )

    context = {"query": query, "results": results}
    return render(request, "books/search.html", context)
