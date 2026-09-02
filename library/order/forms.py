from django import forms
from .models import Order
from book.models import Book


class OrderCreateForm(forms.ModelForm):
    """Form for users to place a new book order."""

    book = forms.ModelChoiceField(
        queryset=Book.objects.filter(count__gt=0).order_by("title"),
        empty_label="Select an available book",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Order
        fields = ["book"]
