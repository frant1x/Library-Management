from django.contrib import admin
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["full_name_display", "country"]
    list_filter = ["country"]
    search_fields = ["first_name", "last_name"]
    ordering = ["last_name", "first_name"]

    fieldsets = (
        (
            "Author Information",
            {
                "fields": (
                    ("first_name", "last_name"),  # виведе поля в один рядок
                    "country",
                ),
            },
        ),
    )

    @admin.display(description="Full Name", ordering="last_name")
    def full_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}"
