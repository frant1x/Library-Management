from django import forms
from .models import User
from django.contrib.auth.password_validation import validate_password

CUSTOM_WIDGETS = {
    "first_name": forms.TextInput(
        attrs={"class": "form-control", "placeholder": "First name"}
    ),
    "last_name": forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Last name"}
    ),
    "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
    "password": forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Password"}
    ),
    "last_login": forms.DateTimeInput(
        attrs={"class": "form-control", "placeholder": "Last login"}
    ),
    "created_at": forms.DateTimeInput(
        attrs={"class": "form-control", "placeholder": "Created at"}
    ),
    "updated_at": forms.DateTimeInput(
        attrs={"class": "form-control", "placeholder": "Updated at"}
    ),
    "is_active": forms.CheckboxInput(
        attrs={"class": "form-check-input", "placeholder": "Active"}
    ),
    "is_superuser": forms.CheckboxInput(
        attrs={"class": "form-check-input", "placeholder": "Superuser"}
    ),
    "is_staff": forms.CheckboxInput(
        attrs={"class": "form-check-input", "placeholder": "Staff"}
    ),
    "role": forms.Select(attrs={"class": "form-select"}),
}


class RegistrationForm(forms.ModelForm):
    """Form for registering a new user."""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        widgets = {key: CUSTOM_WIDGETS[key] for key in fields}

    def clean_email(self):
        email = self.cleaned_data.get("email")
        return email.lower().strip() if email else email

    # def clean_password(self):
    #     """Validate the password using Django's built-in validators."""
    #     password = self.cleaned_data.get("password")
    #     validate_password(password)
    #     return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.role = User.Roles.VISITOR
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Form for logging in a user."""

    email = forms.EmailField(widget=CUSTOM_WIDGETS["email"])
    password = forms.CharField(widget=CUSTOM_WIDGETS["password"])


class UserForm(forms.ModelForm):
    """Form for updating user information."""

    created_at = forms.DateTimeField(
        label="Created_at",
        disabled=True,
        required=False,
        widget=CUSTOM_WIDGETS["created_at"],
    )
    updated_at = forms.DateTimeField(
        label="Updated_at",
        disabled=True,
        required=False,
        widget=CUSTOM_WIDGETS["updated_at"],
    )

    class Meta:
        model = User
        fields = "__all__"
        widgets = CUSTOM_WIDGETS

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        readonly_fields = [
            "password",
            "role",
            "last_login",
            "is_active",
            "is_superuser",
            "is_staff",
        ]

        for field_name in readonly_fields:
            self.fields[field_name].disabled = True

        if self.instance and self.instance.pk:
            self.fields["created_at"].initial = self.instance.created_at
            self.fields["updated_at"].initial = self.instance.updated_at
