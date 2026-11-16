"""Тесты приложения users."""

from django.test import TestCase
from .models import User


class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create(name="Анна", created_at="01.09.2026")
        self.assertEqual(user.name, "Анна")
        self.assertEqual(str(user), "Анна")

    def test_books_related_name(self):
        from books.models import Book
        user = User.objects.create(name="Анна")
        Book.objects.create(
            title="Книга", author="Автор", year=2000,
            status="читаю", user=user,
        )
        self.assertEqual(user.books.count(), 1)
