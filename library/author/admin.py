from django.contrib import admin

from .models import Author


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "surname", "get_books"]

    def get_books(self, obj):
        return ", ".join([f"{book.name}" for book in obj.books.all()])

    get_books.short_description = "Books"
    search_fields = ["name", "surname"]
    list_filter = ["books"]
    readonly_fields = ["get_books"]
    fieldsets = [
        (
            "Personal info",
            {
                "fields": [
                    "name",
                    "surname",
                    "patronymic",
                ],
            },
        ),
        (None, {"fields": ["get_books"]}),
    ]


admin.site.register(Author, AuthorAdmin)
