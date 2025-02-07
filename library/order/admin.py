from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ["book", "user", "created_at", "plated_end_at", "returned"]
    list_filter = ["book", "user", "created_at", "plated_end_at"]
    readonly_fields = ["created_at"]
    fieldsets = [
        (
            None,
            {
                "fields": ["book", "user"],
            },
        ),
        (
            "Date information",
            {
                "classes": ["collapse"],
                "fields": ["created_at", "plated_end_at", "end_at"],
            },
        ),
    ]


admin.site.register(Order, OrderAdmin)
