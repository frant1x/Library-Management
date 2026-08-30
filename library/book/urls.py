from django.urls import path

from . import views

app_name = "book"
urlpatterns = [
    path("", views.BookListView.as_view(), name="all_books"),
    path("add/", views.BookCreateView.as_view(), name="add_book"),
    path("<int:pk>/", views.BookDetailView.as_view(), name="specific_book"),
    path("<int:pk>/edit/", views.BookUpdateView.as_view(), name="edit_book"),
]
