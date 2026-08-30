from django.db import models
from author.models import Author


class Book(models.Model):
    """Represents a book available in the library catalog."""

    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="books")
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        """String representation of the Book object"""
        return f"{self.title} ({self.author.last_name})"

    @property
    def is_available(self):
        """Check if at least one copy of the book is in stock."""
        return self.count > 0
