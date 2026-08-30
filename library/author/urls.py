from django.urls import path

from . import views

app_name = "author"
urlpatterns = [
    path("", views.AuthorListView.as_view(), name="all_authors"),
    path("create/", views.AuthorCreateView.as_view(), name="create_author"),
    path("<int:pk>/edit", views.AuthorUpdateView.as_view(), name="edit_author"),
    path("<int:pk>/delete", views.AuthorDeleteView.as_view(), name="delete_author"),
]
