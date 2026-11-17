"""Заполнение slug для уже существующих книг."""

from django.db import migrations
from django.utils.text import slugify
from unidecode import unidecode


def populate_book_slugs(apps, schema_editor):
    """Сформировать slug из транслитерации названия и первичного ключа."""
    Book = apps.get_model("books", "Book")
    for book in Book.objects.all().order_by("pk"):
        base_slug = slugify(unidecode(book.title)) or "book"
        book.slug = f"{base_slug}-{book.pk}"
        book.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0004_book_slug"),
    ]

    operations = [
        migrations.RunPython(populate_book_slugs, migrations.RunPython.noop),
    ]
