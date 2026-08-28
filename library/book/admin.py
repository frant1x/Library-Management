from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for the Book model."""

    list_display = ["title", "author", "count", "is_available_display"]
    list_filter = ["author"]
    search_fields = ["title", "author__first_name", "author__last_name"]
    list_select_related = ["author"]
    autocomplete_fields = ["author"]
    ordering = ["title"]

    fieldsets = (
        (
            "Book Details",
            {
                "fields": (
                    "title",
                    "author",
                    "count",
                    "description",
                ),
            },
        ),
    )

    @admin.display(boolean=True, description="Available")
    def is_available_display(self, obj):
        """Display stock availability as a boolean icon."""
        return obj.is_available
