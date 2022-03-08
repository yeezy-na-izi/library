from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django import forms
from user.models import CustomUser


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]


class ChangeUserPasswordForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = [
            'old_password',
            'new_password1',
            'new_password2'
        ]


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password1',
        ]
