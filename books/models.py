from django.db import models
from django.db.models import Case, Value, When
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

from users.models import User


class BookQuerySet(models.QuerySet):
    """Собственные методы для частых запросов к книгам."""

    def active(self):
        """Книги в списке чтения: все, кроме отложенных."""
        return self.exclude(status=self.model.Status.ON_HOLD)

    def read(self):
        """Прочитанные книги."""
        return self.filter(status=self.model.Status.READ)

    def reading(self):
        """Книги, которые читаются сейчас."""
        return self.filter(status=self.model.Status.READING)


class BookManager(models.Manager.from_queryset(BookQuerySet)):
    """Менеджер книг с методами BookQuerySet."""

    pass


class Book(models.Model):
    class Status(models.TextChoices):
        WANT_TO_READ = "want_to_read", "Хочу прочитать"
        READING = "reading", "Читаю"
        READ = "read", "Прочитано"
        ON_HOLD = "on_hold", "Отложено"

    CLASSIC_BEFORE_YEAR = 1950

    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.CharField(max_length=200, verbose_name="Автор")
    year = models.IntegerField(verbose_name="Год издания")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.WANT_TO_READ,
        verbose_name="Статус",
    )
    date_added = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Дата добавления",
    )

    slug = models.SlugField(
        max_length=180,
        editable=False,
        verbose_name="URL-идентификатор",
    )

    is_classic = models.GeneratedField(
        expression=Case(
            When(year__lt=CLASSIC_BEFORE_YEAR, then=Value(True)),
            default=Value(False),
            output_field=models.BooleanField(),
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name="Классика",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="books",
        verbose_name="Пользователь",
    )

    objects = BookManager()

    class Meta:
        ordering = ["title"]
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return f"{self.title} — {self.author}"

    @property
    def is_read(self):
        """Признак «книга прочитана»."""
        return self.status == self.Status.READ

    def save(self, *args, **kwargs):
        """Сохранить книгу; slug формируется при первом сохранении."""
        if not self.slug:
            base_slug = slugify(unidecode(self.title)) or "book"
            if self.pk:
                self.slug = f"{base_slug}-{self.pk}"
            else:
                super().save(*args, **kwargs)
                self.slug = f"{base_slug}-{self.pk}"
                super().save(update_fields=["slug"])
                return
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Адрес подробной страницы книги по slug."""
        return reverse("books:detail", kwargs={"slug": self.slug})
