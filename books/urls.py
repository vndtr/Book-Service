from django.urls import path

from . import views

app_name = "books"

urlpatterns = [
    path("", views.books, name="list"),
    path("create/", views.book_create, name="create"),
    path("stats/", views.stats, name="stats"),
    path("search/", views.search_books, name="search"),
    path("<int:book_id>/edit/", views.book_update, name="update"),
    path("<int:book_id>/hold/", views.book_hold, name="hold"),
    path(
        "<int:book_id>/change_status/",
        views.change_status,
        name="change_status",
    ),
    path("<slug:slug>/", views.book_detail, name="detail"),
]
