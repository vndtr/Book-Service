from django.db import models
from users.models import User


class Book(models.Model):
    STATUS_CHOICES = [
        ('хочу прочитать', 'Хочу прочитать'),
        ('читаю', 'Читаю'),
        ('прочитано', 'Прочитано'),
        ('отложено', 'Отложено'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.CharField(max_length=200, verbose_name="Автор")
    year = models.IntegerField(verbose_name="Год издания")
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='хочу прочитать'
    )
    date_added = models.CharField(max_length=20, blank=True)

    # Связь "многие к одному" с вашей моделью User
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='books',
        verbose_name="Пользователь"
    )

    class Meta:
        ordering = ['title']
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return f"{self.title} — {self.author}"
