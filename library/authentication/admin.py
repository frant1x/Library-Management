from django.contrib import admin

from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "email",
        "created_at",
        "role",
        "is_superuser",
    ]
    list_filter = ["first_name", "last_name", "created_at", "role", "is_superuser"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "middle_name",
                    ("email", "password"),
                ],
            },
        ),
        (
            "Date options",
            {
                "classes": ["collapse"],
                "fields": ["created_at", "last_login", "updated_at"],
            },
        ),
        (
            "Permissions",
            {
                "classes": ["collapse"],
                "fields": ["role", ("is_active", "is_superuser", "is_staff")],
            },
        ),
    ]
    search_fields = ["first_name", "last_name"]


admin.site.register(CustomUser, UserAdmin)
