from django.urls import path

from . import views

app_name = "author"
urlpatterns = [
    path("", views.all_authors, name="all_authors"),
    path("create/", views.create_author, name="create_author"),
    path("edit/<int:author_id>/", views.edit_author, name="edit_author"),
    path("delete/<int:author_id>/", views.delete_author, name="delete_author"),
]
