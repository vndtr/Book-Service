"""Формы приложения books: фильтрация списка, создание и редактирование."""

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from users.models import User

from .models import Book

MIN_YEAR = 1000
MAX_COVER_SIZE = 2 * 1024 * 1024


def validate_year_range(value):
    """Валидатор-функция: год издания должен быть не меньше MIN_YEAR."""
    if value < MIN_YEAR:
        raise ValidationError(
            f"Год издания не может быть меньше {MIN_YEAR}."
        )


class BookFilterForm(forms.Form):
    """Форма фильтрации и сортировки списка книг (GET-параметры)."""

    status = forms.ChoiceField(
        required=False,
        label="Статус",
        choices=[("", "Все статусы")] + Book.Status.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    year_from = forms.IntegerField(
        required=False,
        label="Год от",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    year_to = forms.IntegerField(
        required=False,
        label="Год до",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.order_by("name"),
        required=False,
        label="Пользователь",
        empty_label="Все пользователи",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    sort = forms.ChoiceField(
        required=False,
        label="Сортировка",
        choices=[
            ("title", "По названию"),
            ("author", "По автору"),
            ("year", "По году (сначала старые)"),
            ("year_desc", "По году (сначала новые)"),
            ("user", "По пользователю"),
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def clean(self):
        """Проверка согласованности диапазона годов."""
        cleaned_data = super().clean()
        year_from = cleaned_data.get("year_from")
        year_to = cleaned_data.get("year_to")
        if year_from and year_to and year_from > year_to:
            raise ValidationError(
                "Начальный год не может быть больше конечного."
            )
        return cleaned_data


class BookForm(forms.ModelForm):
    """Форма создания и редактирования книги на основе модели Book."""

    class Meta:
        model = Book
        # Статус, slug, дата добавления и is_classic пользователь
        # напрямую не задает: их определяет приложение или база данных.
        fields = ["title", "author", "year", "user", "cover"]
        labels = {
            "title": "Название",
            "author": "Автор",
            "year": "Год издания",
            "user": "Пользователь",
            "cover": "Обложка",
        }
        help_texts = {
            "title": "Укажите название книги.",
            "author": "Укажите автора книги.",
            "year": "Год первого издания, например 1869.",
            "user": "Выберите, чей это список чтения.",
            "cover": "Необязательно. Изображение JPG или PNG до 2 МБ.",
        }
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Например: Война и мир",
            }),
            "author": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Например: Лев Толстой",
            }),
            "year": forms.NumberInput(attrs={"class": "form-control"}),
            "user": forms.Select(attrs={"class": "form-select"}),
            "cover": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Валидатор-функция подключается к полю года издания.
        self.fields["year"].validators.append(validate_year_range)

    def clean_title(self):
        """Название: убираем лишние пробелы, пустое значение запрещено."""
        title = " ".join(self.cleaned_data["title"].split())
        if not title:
            raise ValidationError("Название не может быть пустым.")
        return title

    def clean_author(self):
        """Автор: убираем лишние пробелы, пустое значение запрещено."""
        author = " ".join(self.cleaned_data["author"].split())
        if not author:
            raise ValidationError("Автор не может быть пустым.")
        return author

    def clean_year(self):
        """Год издания не может быть в будущем."""
        year = self.cleaned_data["year"]
        if year > timezone.localdate().year:
            raise ValidationError("Год издания не может быть в будущем.")
        return year

    def clean_cover(self):
        """Ограничиваем размер загружаемой обложки."""
        cover = self.cleaned_data.get("cover")
        if cover and hasattr(cover, "size") and cover.size > MAX_COVER_SIZE:
            raise ValidationError("Размер файла не должен превышать 2 МБ.")
        return cover
