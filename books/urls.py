"""Маршруты приложения books."""

from django.urls import path

from . import views

app_name = "books"

urlpatterns = [
    path("", views.books, name="list"),
    path("<int:book_id>/", views.book_detail, name="detail"),
]
