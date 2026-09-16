from django import forms
from django_countries.widgets import CountrySelectWidget
from .models import Author


class AuthorForm(forms.ModelForm):
    """Form for creating and updating Author instances."""

    class Meta:
        model = Author
        fields = "__all__"
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last name"}
            ),
            "country": CountrySelectWidget(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.col_class = "col-12"
        self.fields["first_name"].col_class = "col-sm-6"
        self.fields["last_name"].col_class = "col-sm-6"
