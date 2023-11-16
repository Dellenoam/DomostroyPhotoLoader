from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
        }),
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'id': 'remember_checkbox',
        }),
    )
