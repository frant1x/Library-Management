from django.urls import path

from . import views

app_name = "author"
urlpatterns = [
    path("", views.AuthorListView.as_view(), name="author_list"),
    path("create/", views.AuthorCreateView.as_view(), name="author_create"),
    path("<int:pk>/update/", views.AuthorUpdateView.as_view(), name="author_update"),
]
