from django import forms
from .models import Order
from authentication.models import User
from book.models import Book


class OrderFilterForm(forms.Form):
    """Form for filtering orders based on book title, user, status, and sorting options."""

    STATUS_CHOICES = [
        ("", "All Statuses"),
        ("active", "Active / Borrowed"),
        ("overdue", "Overdue"),
        ("returned", "Returned"),
    ]

    SORT_CHOICES = [
        ("created_desc", "Newest loans first"),
        ("created_asc", "Oldest loans first"),
        ("due_asc", "Deadline (Earliest)"),
        ("due_desc", "Deadline (Latest)"),
        ("returned_desc", "Recently returned"),
    ]

    book = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-sm",
                "placeholder": "Book title...",
            }
        ),
    )

    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        empty_label="All Readers",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )

    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )

    def __init__(self, *args, is_staff=False, **kwargs):
        super().__init__(*args, **kwargs)

        if is_staff:
            self.fields["book"].col_class = "col-md-3"
            self.fields["user"].col_class = "col-md-3"
            self.fields["status"].col_class = "col-md-2"
            self.fields["sort"].col_class = "col-md-2"
            self.button_col_class = "col-md-2"
        else:
            self.fields.pop("user", None)

            self.fields["book"].col_class = "col-md-3"
            self.fields["status"].col_class = "col-md-4"
            self.fields["sort"].col_class = "col-md-3"
            self.button_col_class = "col-md-2"
