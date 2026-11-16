"""Тесты приложения books (ORM и админка)."""

from django.test import TestCase
from django.contrib.admin.sites import site as admin_site

from users.models import User
from .models import Book


class BookModelTests(TestCase):
    """Тесты ORM-модели Book."""

    def setUp(self):
        self.user = User.objects.create(name="Тест", created_at="01.01.2026")
        self.book = Book.objects.create(
            title="Книга",
            author="Автор",
            year=2000,
            status="читаю",
            user=self.user,
        )

    def test_book_str(self):
        self.assertEqual(str(self.book), "Книга — Автор")

    def test_filter_by_status(self):
        self.assertEqual(Book.objects.filter(status="читаю").count(), 1)

    def test_select_related(self):
        qs = Book.objects.select_related("user").filter(pk=self.book.pk)
        self.assertEqual(qs.first().user.name, "Тест")

    def test_aggregate_avg_year(self):
        from django.db.models import Avg
        self.assertEqual(Book.objects.aggregate(avg=Avg("year"))["avg"], 2000)


class BookAdminTests(TestCase):
    """Тесты регистрации модели в админке."""

    def test_book_registered(self):
        self.assertIn(Book, admin_site._registry)

    def test_user_registered(self):
        from users.models import User as DomainUser
        self.assertIn(DomainUser, admin_site._registry)
