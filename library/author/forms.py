from django.forms import ModelForm
from django import forms

from .models import Author


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Name"}
            ),
            "surname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Surname"}
            ),
            "patronymic": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Patronymic"}
            ),
            "books": forms.SelectMultiple(attrs={"class": "form-select"}),
        }
