from django.urls import path

from . import views

app_name = "books"

urlpatterns = [
    path("", views.books, name="list"),
    path("stats/", views.stats, name="stats"),
    path("search/", views.search_books, name="search"),
    path("<int:book_id>/", views.book_detail, name="detail"),
    path(
        "<int:book_id>/change_status/",
        views.change_status,
        name="change_status",
    ),
]
