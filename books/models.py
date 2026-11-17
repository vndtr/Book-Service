from django.db import models
from django.db.models import Case, Value, When
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

from users.models import User


class BookQuerySet(models.QuerySet):
    """Повторно используемые условия отбора книг."""

    def active(self):
        """Книги в списке чтения: все, кроме отложенных."""
        return self.exclude(status=self.model.Status.ON_HOLD)

    def want_to_read(self):
        """Книги, которые планируется прочитать."""
        return self.filter(status=self.model.Status.WANT_TO_READ)

    def reading(self):
        """Книги, которые читаются сейчас."""
        return self.filter(status=self.model.Status.READING)

    def read(self):
        """Прочитанные книги."""
        return self.filter(status=self.model.Status.READ)

    def on_hold(self):
        """Отложенные книги."""
        return self.filter(status=self.model.Status.ON_HOLD)


class BookManager(models.Manager.from_queryset(BookQuerySet)):
    """Менеджер книг с методами BookQuerySet."""


class Book(models.Model):
    class Status(models.TextChoices):
        WANT_TO_READ = "want_to_read", "Хочу прочитать"
        READING = "reading", "Читаю"
        READ = "read", "Прочитано"
        ON_HOLD = "on_hold", "Отложено"

    # Книги, изданные раньше этого года, считаются классикой.
    CLASSIC_BEFORE_YEAR = 1950

    title = models.CharField(
        max_length=200,
        verbose_name="Название",
        help_text="Укажите название книги.",
    )
    author = models.CharField(
        max_length=200,
        verbose_name="Автор",
        help_text="Укажите автора книги.",
    )
    year = models.IntegerField(
        verbose_name="Год издания",
        help_text="Год первого издания, например 1869.",
    )
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
        unique=True,
        editable=False,
        verbose_name="URL-идентификатор",
    )
    cover = models.ImageField(
        upload_to="covers/",
        blank=True,
        null=True,
        verbose_name="Обложка",
        help_text="Необязательно. Изображение JPG или PNG до 2 МБ.",
    )
    # Вычисляемое поле: значение формируется базой данных по году издания.
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

    # Связь "многие к одному" с вашей моделью User
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='books',
        verbose_name="Пользователь",
        help_text="Пользователь, которому принадлежит книга.",
    )

    objects = BookManager()

    class Meta:
        ordering = ['title']
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return f"{self.title} — {self.author}"

    def save(self, *args, **kwargs):
        """Сохранить книгу; slug формируется при первом сохранении."""
        if not self.slug:
            # Сначала транслитерируем название, затем приводим к виду URL.
            base_slug = slugify(unidecode(self.title)) or "book"
            if self.pk:
                self.slug = f"{base_slug}-{self.pk}"
            else:
                # У новой книги нет pk: сохраняем, чтобы получить ID,
                # затем добавляем его к slug и сохраняем только slug.
                super().save(*args, **kwargs)
                self.slug = f"{base_slug}-{self.pk}"
                super().save(update_fields=["slug"])
                return
        super().save(*args, **kwargs)

    @property
    def is_read(self):
        """Признак «книга прочитана»."""
        return self.status == self.Status.READ

    def put_on_hold(self):
        """Отложить книгу: меняется статус, запись остается в базе."""
        self.status = self.Status.ON_HOLD
        self.save(update_fields=["status"])

    def get_absolute_url(self):
        """Адрес подробной страницы книги по slug."""
        return reverse("books:detail", kwargs={"slug": self.slug})
