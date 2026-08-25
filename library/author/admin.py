from django.contrib import admin
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "country"]
    list_filter = ["country"]
    search_fields = ["first_name", "last_name"]
    ordering = ["last_name", "first_name"]
    fields = ["first_name", "last_name", "country"]
