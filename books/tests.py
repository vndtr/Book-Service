"""Тесты приложения books: модели, ORM, админка, формы и представления."""

import shutil
import tempfile
from io import BytesIO

from django.contrib.auth import get_user_model
from django.contrib.admin.sites import site as admin_site
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import ProtectedError
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from users.models import User

from .forms import BookFilterForm, BookForm
from .models import Book


def make_book(user, title="Dune", author="Frank Herbert", year=1965,
              status=Book.Status.WANT_TO_READ):
    """Создать книгу для тестов."""
    return Book.objects.create(
        title=title, author=author, year=year, status=status, user=user,
    )


def make_image_file(name="cover.png"):
    """Создать небольшое корректное изображение для проверки загрузки."""
    buffer = BytesIO()
    Image.new("RGB", (10, 10), (200, 50, 50)).save(buffer, format="PNG")
    return SimpleUploadedFile(
        name, buffer.getvalue(), content_type="image/png"
    )


class BookModelTests(TestCase):
    """Модель Book: статусы, slug, вычисляемое поле, связи."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(name="Алена")

    def test_str(self):
        book = make_book(self.user)
        self.assertEqual(str(book), "Dune — Frank Herbert")

    def test_default_status_is_want_to_read(self):
        book = Book.objects.create(
            title="X", author="Y", year=2000, user=self.user,
        )
        self.assertEqual(book.status, Book.Status.WANT_TO_READ)
        self.assertEqual(book.get_status_display(), "Хочу прочитать")

    def test_slug_created_automatically_with_pk(self):
        book = make_book(self.user, title="Dune Messiah")
        self.assertEqual(book.slug, f"dune-messiah-{book.pk}")

    def test_slug_unique_for_same_titles(self):
        first = make_book(self.user, title="Dune")
        second = make_book(self.user, title="Dune")
        self.assertNotEqual(first.slug, second.slug)

    def test_slug_for_cyrillic_title_is_latin(self):
        book = make_book(self.user, title="Война и мир", year=1869)
        self.assertRegex(book.slug, r"^[a-z0-9-]+-\d+$")

    def test_slug_not_changed_on_title_edit(self):
        book = make_book(self.user, title="Dune")
        old_slug = book.slug
        book.title = "Another"
        book.save()
        self.assertEqual(book.slug, old_slug)

    def test_get_absolute_url(self):
        book = make_book(self.user, title="Dune")
        self.assertEqual(book.get_absolute_url(), f"/books/{book.slug}/")

    def test_generated_field_is_classic(self):
        old = make_book(self.user, title="Old", year=1949)
        new = make_book(self.user, title="New", year=1950)
        old.refresh_from_db()
        new.refresh_from_db()
        self.assertTrue(old.is_classic)
        self.assertFalse(new.is_classic)
        new.year = 1900
        new.save()
        new.refresh_from_db()
        self.assertTrue(new.is_classic)

    def test_put_on_hold_keeps_record(self):
        book = make_book(self.user)
        book.put_on_hold()
        book.refresh_from_db()
        self.assertEqual(book.status, Book.Status.ON_HOLD)
        self.assertTrue(Book.objects.filter(pk=book.pk).exists())

    def test_is_read_property(self):
        book = make_book(self.user, status=Book.Status.READ)
        self.assertTrue(book.is_read)

    def test_user_with_books_is_protected(self):
        make_book(self.user)
        with self.assertRaises(ProtectedError):
            self.user.delete()

    def test_related_name_books(self):
        make_book(self.user)
        self.assertEqual(self.user.books.count(), 1)


class BookQuerySetTests(TestCase):
    """Методы пользовательского QuerySet и менеджера."""

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(name="Алена")
        make_book(user, title="A", status=Book.Status.WANT_TO_READ)
        make_book(user, title="B", status=Book.Status.READING)
        make_book(user, title="C", status=Book.Status.READ)
        make_book(user, title="D", status=Book.Status.ON_HOLD)

    def test_status_methods(self):
        self.assertEqual(Book.objects.want_to_read().count(), 1)
        self.assertEqual(Book.objects.reading().count(), 1)
        self.assertEqual(Book.objects.read().count(), 1)
        self.assertEqual(Book.objects.on_hold().count(), 1)

    def test_active_excludes_on_hold(self):
        titles = set(Book.objects.active().values_list("title", flat=True))
        self.assertEqual(titles, {"A", "B", "C"})

    def test_methods_can_be_chained(self):
        self.assertEqual(Book.objects.active().reading().count(), 1)
        self.assertEqual(Book.objects.on_hold().active().count(), 0)


class ContextProcessorTests(TestCase):
    """Контекстный процессор book_context."""

    def test_values_available_on_pages(self):
        user = User.objects.create(name="Алена")
        make_book(user)
        make_book(user, title="Two")
        for name in ("homepage:index", "books:list", "books:stats"):
            response = self.client.get(reverse(name))
            self.assertEqual(response.context["site_name"], "Book Service")
            self.assertEqual(response.context["books_count"], 2)
        self.assertContains(self.client.get(reverse("books:list")),
                            "Книги (2)")


class BookAdminTests(TestCase):
    """Настройка Django Admin."""

    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser(
            "admin", "admin@example.com", "pass12345",
        )
        cls.user = User.objects.create(name="Алена")
        cls.book = make_book(cls.user, title="Dune", year=1965)

    def setUp(self):
        self.client.force_login(self.admin)

    def test_models_registered_once(self):
        self.assertIn(Book, admin_site._registry)
        self.assertIn(User, admin_site._registry)

    def test_admin_pages_open(self):
        for url in (
            reverse("admin:books_book_changelist"),
            reverse("admin:books_book_change", args=[self.book.pk]),
            reverse("admin:users_user_changelist"),
            reverse("admin:users_user_change", args=[self.user.pk]),
        ):
            self.assertEqual(self.client.get(url).status_code, 200)

    def test_book_search_by_related_user_and_cyrillic(self):
        url = reverse("admin:books_book_changelist")
        response = self.client.get(url, {"q": "алена"})
        self.assertContains(response, "Dune")

    def test_user_page_has_inline_books(self):
        response = self.client.get(
            reverse("admin:users_user_change", args=[self.user.pk])
        )
        self.assertContains(response, "Dune")

    def test_site_link_in_list(self):
        response = self.client.get(reverse("admin:books_book_changelist"))
        self.assertContains(response, self.book.get_absolute_url())

    def test_put_on_hold_action(self):
        self.client.post(
            reverse("admin:books_book_changelist"),
            {
                "action": "put_on_hold_action",
                "_selected_action": [self.book.pk],
            },
        )
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, Book.Status.ON_HOLD)

    def test_restore_action(self):
        self.book.put_on_hold()
        self.client.post(
            reverse("admin:books_book_changelist"),
            {
                "action": "restore_to_plan_action",
                "_selected_action": [self.book.pk],
            },
        )
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, Book.Status.WANT_TO_READ)

    def test_list_select_related_limits_queries(self):
        for i in range(5):
            make_book(self.user, title=f"Book {i}")
        url = reverse("admin:books_book_changelist")
        with self.assertNumQueries(9):
            self.client.get(url)


class BookFormsTests(TestCase):
    """Валидация форм фильтрации и создания книги."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(name="Алена")

    def data(self, **kwargs):
        data = {
            "title": "Dune", "author": "Frank Herbert",
            "year": 1965, "user": self.user.pk,
        }
        data.update(kwargs)
        return data

    def test_filter_form_valid_and_empty(self):
        self.assertTrue(BookFilterForm({}).is_valid())
        self.assertTrue(BookFilterForm({"status": "reading"}).is_valid())

    def test_filter_form_invalid_values(self):
        for params in (
            {"status": "unknown"},
            {"year_from": "abc"},
            {"user": "999999"},
            {"sort": "unknown"},
            {"year_from": "2000", "year_to": "1900"},
        ):
            self.assertFalse(BookFilterForm(params).is_valid(), params)

    def test_book_form_valid(self):
        self.assertTrue(BookForm(self.data()).is_valid())

    def test_book_form_status_not_in_fields(self):
        self.assertNotIn("status", BookForm().fields)
        self.assertNotIn("slug", BookForm().fields)

    def test_year_in_future_rejected(self):
        year = timezone.localdate().year + 1
        form = BookForm(self.data(year=year))
        self.assertFalse(form.is_valid())
        self.assertIn("year", form.errors)

    def test_year_too_small_rejected(self):
        form = BookForm(self.data(year=999))
        self.assertFalse(form.is_valid())
        self.assertIn("year", form.errors)

    def test_blank_title_rejected(self):
        form = BookForm(self.data(title="   "))
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_title_spaces_normalized(self):
        form = BookForm(self.data(title="  Dune   Messiah "))
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "Dune Messiah")


class BookListViewTests(TestCase):
    """Список книг: фильтры, сортировка, пагинация."""

    @classmethod
    def setUpTestData(cls):
        cls.alena = User.objects.create(name="Алена")
        cls.ivan = User.objects.create(name="Иван")
        data = [
            ("Book A", "Author A", 1900, "reading", cls.alena),
            ("Book B", "Author B", 1950, "read", cls.alena),
            ("Book C", "Author C", 1990, "want_to_read", cls.alena),
            ("Book D", "Author D", 2000, "on_hold", cls.alena),
            ("Book E", "Author E", 2010, "reading", cls.alena),
            ("Book F", "Author F", 2020, "reading", cls.ivan),
        ]
        for title, author, year, status, user in data:
            make_book(user, title, author, year, status)

    def get(self, **params):
        return self.client.get(reverse("books:list"), params)

    def test_default_list_shows_only_active_books(self):
        response = self.get()
        self.assertEqual(response.context["total"], 5)
        titles = [b["title"] for b in response.context["books"]]
        self.assertNotIn("Book D", titles)

    def test_pagination_five_per_page(self):
        response = self.get()
        self.assertEqual(len(response.context["books"]), 5)
        make_book(self.alena, "Book G", "Author G", 2021, "read")
        response = self.get(page=2)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(len(response.context["books"]), 1)

    def test_filter_status(self):
        response = self.get(status="reading")
        self.assertEqual(response.context["total"], 3)

    def test_on_hold_status_uses_on_hold_queryset(self):
        response = self.get(status="on_hold")
        titles = [b["title"] for b in response.context["books"]]
        self.assertEqual(titles, ["Book D"])

    def test_filter_years_and_user(self):
        response = self.get(year_from=1950, year_to=2010)
        self.assertEqual(response.context["total"], 3)
        response = self.get(user=self.ivan.pk)
        self.assertEqual(response.context["total"], 1)

    def test_combined_filters(self):
        response = self.get(status="reading", user=self.alena.pk)
        self.assertEqual(response.context["total"], 2)

    def test_invalid_params_show_error_without_exception(self):
        for params in (
            {"year_from": "abc"}, {"status": "xxx"},
            {"user": "999999"}, {"sort": "unknown"},
            {"year_from": "2000", "year_to": "1900"},
        ):
            response = self.get(**params)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.context["error"],
                "Проверьте введённые значения фильтров.",
            )
            self.assertEqual(response.context["total"], 5)

    def test_sort_options(self):
        response = self.get(sort="year_desc")
        years = [b["year"] for b in response.context["books"]]
        self.assertEqual(years, sorted(years, reverse=True))
        response = self.get(sort="user")
        names = [b["user_name"] for b in response.context["books"]]
        self.assertEqual(names, sorted(names))

    def test_pagination_links_keep_parameters(self):
        for i in range(6):
            make_book(self.alena, f"Extra {i}", year=1980 + i)
        response = self.get(sort="year_desc", status="")
        self.assertContains(response, "pagination")
        self.assertContains(response, "sort=year_desc")
        self.assertContains(response, "page=2")

    def test_page_not_a_number(self):
        self.assertEqual(self.get(page="abc").status_code, 200)

    def test_values_include_related_user_name(self):
        response = self.get()
        self.assertIn("user_name", response.context["books"][0])

    def test_list_query_count(self):
        with self.assertNumQueries(4):
            self.get()


class BookDetailAndHoldTests(TestCase):
    """Страница книги, 404, отложить, смена статуса."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(name="Алена")
        cls.book = make_book(cls.user, title="Dune", year=1965)

    def test_detail_by_slug(self):
        response = self.client.get(self.book.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Алена")
        self.assertContains(response, "Обложка не загружена")

    def test_detail_loads_book_and_user_with_one_query(self):
        # Второй запрос - счетчик книг из контекстного процессора.
        with self.assertNumQueries(2):
            self.client.get(self.book.get_absolute_url())

    def test_detail_404_for_unknown_slug(self):
        url = reverse("books:detail", kwargs={"slug": "no-such-book-1"})
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_hold_requires_post(self):
        url = reverse("books:hold", args=[self.book.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, Book.Status.WANT_TO_READ)

    def test_hold_changes_status_and_keeps_record(self):
        url = reverse("books:hold", args=[self.book.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("books:list"))
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, Book.Status.ON_HOLD)
        # Отложенная книга исчезает из списка и повторно не откладывается.
        self.assertEqual(
            self.client.get(reverse("books:list")).context["total"], 0
        )
        self.assertEqual(self.client.post(url).status_code, 404)

    def test_hold_is_csrf_protected(self):
        client = Client(enforce_csrf_checks=True)
        url = reverse("books:hold", args=[self.book.pk])
        self.assertEqual(client.post(url).status_code, 403)
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, Book.Status.WANT_TO_READ)

    def test_change_status(self):
        url = reverse("books:change_status", args=[self.book.pk])
        self.client.post(url, {"status": "read"})
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, Book.Status.READ)
        self.client.post(url, {"status": "bad"})
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, Book.Status.READ)
        self.assertEqual(self.client.get(url).status_code, 405)


class BookCreateUpdateTests(TestCase):
    """Создание и редактирование книг через ModelForm."""

    @classmethod
    def setUpTestData(cls):
        cls.alena = User.objects.create(name="Алена")
        cls.ivan = User.objects.create(name="Иван")

    def payload(self, **kwargs):
        data = {
            "title": "Dune", "author": "Frank Herbert",
            "year": 1965, "user": self.alena.pk,
        }
        data.update(kwargs)
        return data

    def test_create_get_shows_empty_form(self):
        response = self.client.get(reverse("books:create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertContains(response, 'enctype="multipart/form-data"')

    def test_create_valid_sets_defaults(self):
        response = self.client.post(reverse("books:create"), self.payload())
        self.assertRedirects(response, reverse("books:list"))
        book = Book.objects.get(title="Dune")
        self.assertEqual(book.status, Book.Status.WANT_TO_READ)
        self.assertEqual(
            book.date_added, timezone.localdate().strftime("%d.%m.%Y")
        )
        self.assertTrue(book.slug.startswith("dune-"))

    def test_create_cannot_set_status_through_form(self):
        self.client.post(
            reverse("books:create"), self.payload(status="read")
        )
        self.assertEqual(
            Book.objects.get(title="Dune").status, Book.Status.WANT_TO_READ
        )

    def test_create_invalid_year_not_saved(self):
        year = timezone.localdate().year + 5
        response = self.client.post(
            reverse("books:create"), self.payload(year=year)
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Год издания не может быть в будущем.")
        self.assertFalse(Book.objects.exists())

    def test_create_duplicate_active_rejected(self):
        make_book(self.alena)
        response = self.client.post(
            reverse("books:create"), self.payload(title="DUNE")
        )
        self.assertContains(
            response, "У этого пользователя уже есть такая книга"
        )
        self.assertEqual(Book.objects.count(), 1)

    def test_create_duplicate_for_other_user_allowed(self):
        make_book(self.alena)
        self.client.post(
            reverse("books:create"), self.payload(user=self.ivan.pk)
        )
        self.assertEqual(Book.objects.count(), 2)

    def test_on_hold_book_does_not_block_new_one(self):
        make_book(self.alena, status=Book.Status.ON_HOLD)
        self.client.post(reverse("books:create"), self.payload())
        self.assertEqual(Book.objects.count(), 2)

    def test_create_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse("books:create"), self.payload())
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Book.objects.exists())

    def test_update_prefilled_and_saved(self):
        book = make_book(self.alena)
        url = reverse("books:update", args=[book.pk])
        response = self.client.get(url)
        self.assertContains(response, 'value="Dune"')
        response = self.client.post(url, self.payload(year=1966))
        self.assertRedirects(response, book.get_absolute_url())
        book.refresh_from_db()
        self.assertEqual(book.year, 1966)
        self.assertEqual(Book.objects.count(), 1)

    def test_update_without_changes_does_not_conflict_with_itself(self):
        book = make_book(self.alena)
        response = self.client.post(
            reverse("books:update", args=[book.pk]), self.payload()
        )
        self.assertEqual(response.status_code, 302)

    def test_update_conflict_with_other_active_book(self):
        make_book(self.alena, title="Other", author="Someone")
        book = make_book(self.alena)
        response = self.client.post(
            reverse("books:update", args=[book.pk]),
            self.payload(title="Other", author="Someone"),
        )
        self.assertContains(
            response, "У этого пользователя уже есть такая книга"
        )
        book.refresh_from_db()
        self.assertEqual(book.title, "Dune")

    def test_update_unknown_and_on_hold_books_return_404(self):
        self.assertEqual(
            self.client.get(reverse("books:update", args=[9999])).status_code,
            404,
        )
        held = make_book(self.alena, status=Book.Status.ON_HOLD)
        self.assertEqual(
            self.client.get(
                reverse("books:update", args=[held.pk])
            ).status_code,
            404,
        )


class CoverUploadTests(TestCase):
    """Загрузка и отображение обложки."""

    def setUp(self):
        self.media_root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.media_root, True)
        self.alena = User.objects.create(name="Алена")

    def test_upload_cover_and_show_on_detail(self):
        with override_settings(MEDIA_ROOT=self.media_root):
            response = self.client.post(
                reverse("books:create"),
                {
                    "title": "Dune", "author": "Frank Herbert",
                    "year": 1965, "user": self.alena.pk,
                    "cover": make_image_file(),
                },
            )
            self.assertEqual(response.status_code, 302)
            book = Book.objects.get(title="Dune")
            self.assertTrue(book.cover.name.startswith("covers/"))
            page = self.client.get(book.get_absolute_url())
            self.assertContains(page, book.cover.url)

    def test_invalid_file_rejected(self):
        with override_settings(MEDIA_ROOT=self.media_root):
            fake = SimpleUploadedFile(
                "x.png", b"not an image", content_type="image/png"
            )
            response = self.client.post(
                reverse("books:create"),
                {
                    "title": "Dune", "author": "Frank Herbert",
                    "year": 1965, "user": self.alena.pk, "cover": fake,
                },
            )
            self.assertEqual(response.status_code, 200)
            self.assertFalse(Book.objects.exists())


class StatsAndSearchTests(TestCase):
    """Статистика и поиск."""

    @classmethod
    def setUpTestData(cls):
        cls.alena = User.objects.create(name="Алена")
        make_book(cls.alena, "A", "Лев Толстой", 1869, "read")
        make_book(cls.alena, "B", "Author B", 1900, "reading")
        make_book(cls.alena, "C", "Author C", 2000, "on_hold")
        make_book(cls.alena, "D", "Author D", 2010, "read")

    def test_stats_counts_by_status(self):
        response = self.client.get(reverse("books:stats"))
        counts = response.context["counts"]
        self.assertEqual(counts["total"], 4)
        self.assertEqual(counts["read"], 2)
        self.assertEqual(counts["reading"], 1)
        self.assertEqual(counts["on_hold"], 1)
        self.assertEqual(counts["want_to_read"], 0)
        self.assertEqual(response.context["years"]["min_year"], 1869)

    def test_search_case_insensitive_cyrillic(self):
        response = self.client.get(
            reverse("books:search"), {"q": "толстой"}
        )
        self.assertEqual(len(response.context["results"]), 1)
        response = self.client.get(reverse("books:search"), {"q": "АЛЕНА"})
        self.assertEqual(len(response.context["results"]), 4)

    def test_search_empty_query(self):
        response = self.client.get(reverse("books:search"))
        self.assertEqual(len(response.context["results"]), 0)
