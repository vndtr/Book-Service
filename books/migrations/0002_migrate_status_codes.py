"""Перенос статусов книг из русских названий в коды TextChoices."""

from django.db import migrations

OLD_TO_NEW = {
    "хочу прочитать": "want_to_read",
    "читаю": "reading",
    "прочитано": "read",
    "отложено": "on_hold",
}


def forwards(apps, schema_editor):
    """Заменить русские значения статуса кодами."""
    Book = apps.get_model("books", "Book")
    for old, new in OLD_TO_NEW.items():
        Book.objects.filter(status=old).update(status=new)


def backwards(apps, schema_editor):
    """Вернуть русские значения статуса при откате миграции."""
    Book = apps.get_model("books", "Book")
    for old, new in OLD_TO_NEW.items():
        Book.objects.filter(status=new).update(status=old)


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
