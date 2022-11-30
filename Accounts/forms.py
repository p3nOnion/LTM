# forms.py
import re

from django.contrib.auth import password_validation
from django_registration.forms import RegistrationForm
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from Accounts.models import Users


class CustomUserCreationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = Users
        fields = ('username', 'email', 'score')


class CustomUserChangeForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = Users
        fields = ('username', 'email', 'score',)
class NewUserForm(forms.Form):
    error_messages = {
        "password_mismatch": ("The two password fields didn’t match."),
        "email_valid": (f'The email address "%s" is not valid')
    }

    email = forms.CharField(max_length=200, required=True, widget=forms.EmailInput(attrs={"autocomplete": "Email"}))
    username = forms.CharField(max_length=200, required=True)
    first_name = forms.CharField(max_length=200, required=False, label=("First name"), )
    last_name = forms.CharField(max_length=200, required=False, label=("Last name"), )
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email):
            # print(f"The email address {email} is not valid")
            raise ValidationError(
                self.error_messages["email_valid"] % email,
                code="email_valid",
            )
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    class Meta:
        model = Users
class EditUser(forms.Form):
    first_name=forms.CharField(max_length=150,required=None)
    last_name=forms.CharField(max_length=150,required=None)
    email=forms.EmailField(max_length=150,required=None)
    class Meta:
        model = Users