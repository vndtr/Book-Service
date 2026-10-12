"""Маршрутизация верхнего уровня проекта Book Service."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("books/", include("books.urls")),
]

# Обработчик ошибки 404 читается только из корневого urls.py
handler404 = "homepage.views.page_not_found"
