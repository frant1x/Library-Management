from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface configuration for managing Order records."""

    list_display = [
        "id",
        "book",
        "user",
        "created_at",
        "planned_end_at",
        "status_badge",
    ]
    list_filter = ["created_at", "planned_end_at"]
    search_fields = ["book__title", "user__last_name"]
    readonly_fields = ["created_at"]

    @admin.display(description="Status")
    def status_badge(self, obj):
        """Render a visual color-coded badge indicating the order state."""
        if obj.is_closed:
            return "CLOSED"
        if obj.is_overdue:
            return "OVERDUE"
        else:
            return "ACTIVE"
