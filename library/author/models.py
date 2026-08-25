from django.db import models
from django_countries.fields import CountryField


class Author(models.Model):
    """Author model representing an author in the library system."""

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150)
    country = CountryField()

    def __str__(self):
        """String representation of the Author object"""
        if self.first_name:
            return f"{self.first_name} {self.last_name}"
        return self.last_name
