from django.urls import path

from . import views

app_name = "book"
urlpatterns = [
    path("", views.BookListView.as_view(), name="book_list"),
    path("add/", views.BookCreateView.as_view(), name="book_create"),
    path("<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("<int:pk>/edit/", views.BookUpdateView.as_view(), name="book_update"),
]
