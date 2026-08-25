from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "created_at",
    ]

    list_filter = ["role", "is_active", "created_at"]

    search_fields = ["last_name"]

    ordering = ["last_name"]

    readonly_fields = ["created_at", "updated_at", "last_login"]

    fieldsets = [
        (
            "Personal Info",
            {
                "fields": [
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                ],
            },
        ),
        (
            "Permissions",
            {
                "fields": [
                    "role",
                    ("is_active", "is_staff", "is_superuser"),
                ],
            },
        ),
        (
            "Important Dates",
            {
                "classes": ["collapse"],
                "fields": ["created_at", "updated_at", "last_login"],
            },
        ),
    ]

    # Форма створення нового користувача через кнопку "+ Додати" в адмінці
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "first_name", "last_name", "password"],
            },
        ),
    ]
