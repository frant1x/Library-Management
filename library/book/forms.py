from django import forms
from .models import Book
from author.models import Author

CUSTOM_WIDGETS = {
    "title": forms.TextInput(
        attrs={"class": "form-control form-control-sm", "placeholder": "Title..."}
    ),
    "description": forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Description",
            "rows": 3,
        }
    ),
    "author": forms.Select(attrs={"class": "form-select form-select-sm"}),
    "count": forms.NumberInput(
        attrs={"class": "form-control", "placeholder": "Number of copies", "min": 0}
    ),
    "count_min": forms.NumberInput(
        attrs={"class": "form-control form-control-sm", "placeholder": "Min copies"}
    ),
    "count_max": forms.NumberInput(
        attrs={"class": "form-control form-control-sm", "placeholder": "Max copies"}
    ),
}


class BookForm(forms.ModelForm):
    """Form for creating and updating Book instances."""

    class Meta:
        model = Book
        fields = ["title", "description", "author", "count"]
        widgets = {key: CUSTOM_WIDGETS[key] for key in fields}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.col_class = "col-12"
        self.fields["count"].col_class = "col-sm-6"


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].col_class = "col-md-3"
        self.fields["author"].col_class = "col-md-3"
        self.fields["count_min"].col_class = "col-md-2"
        self.fields["count_max"].col_class = "col-md-2"
        self.button_col_class = "col-md-2"
