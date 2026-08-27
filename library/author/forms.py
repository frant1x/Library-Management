from django import forms
from django_countries.widgets import CountrySelectWidget
from .models import Author


class AuthorForm(forms.ModelForm):
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
