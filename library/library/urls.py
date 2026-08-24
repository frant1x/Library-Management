from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("auth/", include("authentication.urls")),
    path("books/", include("book.urls")),
    path("orders/", include("order.urls")),
    path("authors/", include("author.urls")),
]
