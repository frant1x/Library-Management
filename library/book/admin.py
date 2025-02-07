from django.contrib import admin

from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ["name", "get_authors", "count", "get_users"]

    def get_authors(self, obj):
        return ", ".join(
            [f"{author.name} {author.surname}" for author in obj.authors.all()]
        )

    def get_users(self, obj):
        return ", ".join(
            [f"{user.first_name} {user.last_name}" for user in obj.users.all()]
        )

    get_authors.short_description = "Authors"
    get_users.short_description = "Borrowed by"
    list_filter = ["name", "count", "authors", "users"]
    readonly_fields = ["get_authors", "get_users"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "get_authors",
                    "description",
                ],
            },
        ),
        (
            "Borrowing Information",
            {
                "classes": ["collapse"],
                "fields": ["get_users", "count"],
            },
        ),
    ]
    search_fields = ["name"]


admin.site.register(Book, BookAdmin)
