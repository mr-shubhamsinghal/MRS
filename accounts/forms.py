from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput
                            (attrs={'placeholder': 'Email Address',
                             'class': 'input100', 'required': ''}))
    password1 = forms.CharField(max_length=254, widget=forms.PasswordInput
                               (attrs={'placeholder': 'Password',
                                'class': 'input100', 'required': ''}))
    password2 = forms.CharField(max_length=254, widget=forms.PasswordInput
                               (attrs={'placeholder': 'Confirm Password',
                                'class': 'input100', 'required': ''}))

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'password1', 'password2',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)