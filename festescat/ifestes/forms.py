from ifestes.models import Usuaris
from django.forms import ModelForm
from django import forms


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Usuaris
        exclude = ['user']
        fields = ['username', 'password', 'email']


class LoginForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Usuaris
        exclude = ['user']
        fields = ['username', 'password']