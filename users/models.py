from django.db import models


class User(models.Model):
    """Пользователь системы учета книг."""

    name = models.CharField(
        max_length=200,
        verbose_name="Имя пользователя",
    )
    created_at = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Дата создания",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name
