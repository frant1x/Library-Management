from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from .models import User

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


class LoginForm(AuthenticationForm):
    """Form for logging in a user."""

    username = forms.EmailField(widget=CUSTOM_WIDGETS["email"])
    password = forms.CharField(widget=CUSTOM_WIDGETS["password"])


class BaseUserForm(forms.ModelForm):
    """Base form with common personal fields."""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = CUSTOM_WIDGETS


class UserProfileForm(BaseUserForm):
    """Form for regular users to update their personal details."""

    new_password = forms.CharField(
        label="Password",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Leave blank to keep current",
            }
        ),
    )

    # def clean(self):
    #     cleaned_data = super().clean()
    #     new_pass = cleaned_data.get("new_password")

    #     if new_pass:
    #         validate_password(new_pass, self.instance)

    #     return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_pass = self.cleaned_data.get("new_password")

        if new_pass:
            user.set_password(new_pass)

        if commit:
            user.save()
        return user


class StaffUserForm(BaseUserForm):
    """Form for librarians to manage reader permissions and statuses."""

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

    class Meta(BaseUserForm.Meta):
        fields = BaseUserForm.Meta.fields + [
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        readonly_fields = [
            "last_login",
            "is_superuser",
            "is_staff",
        ]

        for field_name in readonly_fields:
            self.fields[field_name].disabled = True

        if self.instance and self.instance.pk:
            self.fields["created_at"].initial = self.instance.created_at
            self.fields["updated_at"].initial = self.instance.updated_at
