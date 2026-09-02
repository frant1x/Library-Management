from datetime import timedelta
from django.utils import timezone
from django.db import models, DataError
from django.contrib import admin
from authentication.models import User
from book.models import Book


class Order(models.Model):
    """Represents a book borrowing transaction by a user."""

    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="orders")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    created_at = models.DateField(auto_now_add=True)
    planned_end_at = models.DateField(default=timezone.localdate() + timedelta(days=14))
    end_at = models.DateField(null=True, blank=True)

    def __str__(self):
        status = "Returned" if self.end_at else "Active"
        return f"Order #{self.pk}: {self.book.title} -> {self.user.email} ({status})"

    @property
    def is_closed(self):
        """Check if the book has already been returned."""
        return self.end_at is not None

    @property
    def is_overdue(self):
        """Check if the active order has passed the planned return deadline."""
        if self.is_closed:
            return False
        return timezone.localdate() > self.planned_end_at
