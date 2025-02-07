from django.forms import ModelForm

from django import forms

from .models import CustomUser

CUSTOM_WIDGETS = {
    "first_name": forms.TextInput(
        attrs={"class": "form-control", "placeholder": "First name"}
    ),
    "middle_name": forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Middle name"}
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


class RegistrationForm(ModelForm):

    class Meta:
        model = CustomUser
        fields = ["first_name", "middle_name", "last_name", "email", "password", "role"]
        widgets = {key: CUSTOM_WIDGETS[key] for key in fields}

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].required = False
        self.fields["middle_name"].required = False
        self.fields["last_name"].required = False

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = True
        if user.role == 1:
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):

    email = forms.EmailField(widget=CUSTOM_WIDGETS["email"])
    password = forms.CharField(widget=CUSTOM_WIDGETS["password"])


class UserForm(ModelForm):
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
        model = CustomUser
        exclude = ["created_at", "updated_at"]
        widgets = CUSTOM_WIDGETS

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["last_login"].disabled = True
        self.fields["is_active"].disabled = True
        self.fields["is_superuser"].disabled = True
        self.fields["is_staff"].disabled = True
        if self.instance and self.instance.pk:
            self.fields["created_at"].initial = self.instance.created_at
            self.fields["updated_at"].initial = self.instance.updated_at

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if user.role == 1:
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False
        if commit:
            user.save()
        return user
