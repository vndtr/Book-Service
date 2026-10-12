"""Маршруты приложения books."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.books, name="books"),
    path("<int:book_id>/", views.book_detail, name="book_detail"),
]
