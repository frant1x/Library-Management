from django import forms
from .models import Book
from author.models import Author

CUSTOM_WIDGETS = {
    "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
    "description": forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Description",
            "rows": 3,
        }
    ),
    "author": forms.Select(attrs={"class": "form-select"}),
    "count": forms.NumberInput(
        attrs={"class": "form-control", "placeholder": "Number of copies", "min": 0}
    ),
    "count_min": forms.NumberInput(
        attrs={"class": "form-control", "placeholder": "Min", "min": 0}
    ),
    "count_max": forms.NumberInput(
        attrs={"class": "form-control", "placeholder": "Max", "min": 0}
    ),
}


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "description", "author", "count"]
        widgets = {key: CUSTOM_WIDGETS[key] for key in fields}


class BookFilterForm(forms.Form):
    """Form for filtering books in the catalog."""

    title = forms.CharField(required=False, widget=CUSTOM_WIDGETS["title"])
    author = forms.ModelChoiceField(
        queryset=Author.objects.all().order_by("last_name", "first_name"),
        required=False,
        empty_label="All Authors",
        widget=CUSTOM_WIDGETS["author"],
    )
    count_min = forms.IntegerField(
        required=False, min_value=0, widget=CUSTOM_WIDGETS["count_min"]
    )
    count_max = forms.IntegerField(
        required=False, min_value=0, widget=CUSTOM_WIDGETS["count_max"]
    )
