from ifestes.models import Usuaris, Organitzadors, Festes
from django.forms import ModelForm
from django import forms


class UserForm(ModelForm):
    username = forms.CharField(label="Introdueix un usuari")
    email = forms.EmailField(label="Introdueix un email")
    password = forms.CharField(label="Introdueix una contrasenya",
        widget=forms.PasswordInput())
    re_password = forms.CharField(label="Torna a introduir la contrasenya",
        widget=forms.PasswordInput())

    class Meta:
        model = Usuaris
        exclude = ['user']
        fields = ['username', 'email', 'password', 're_password']

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if not re_password:
            raise forms.ValidationError("You must confirm your password")
        if password != re_password:
            raise forms.ValidationError("Your passwords do not match")
        return re_password


class UserFormEdit(ModelForm):
    username = forms.CharField(label="Introdueix un nou usuari")
    email = forms.EmailField(label="Introdueix un nou email")
    password = forms.CharField(label="Introdueix una nova contrasenya",
        widget=forms.PasswordInput())
    re_password = forms.CharField(label="Torna a introduir la nova contrasenya",
        widget=forms.PasswordInput())

    class Meta:
        model = Usuaris
        exclude = ['user']
        fields = ['username', 'email', 'password', 're_password']

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if not re_password:
            raise forms.ValidationError("You must confirm your password")
        if password != re_password:
            raise forms.ValidationError("Your passwords do not match")
        return re_password


class LoginForm(ModelForm):
    username = forms.CharField(label="Introdueix el teu usuari")
    password = forms.CharField(label="Introdueix la teva contrasenya",
        widget=forms.PasswordInput())

    class Meta:
        model = Usuaris
        exclude = ['user']
        fields = ['username', 'password']


class OrgForm(ModelForm):
    empresa = forms.CharField(label="Introdueix el nom de la empresa")

    class Meta:
        model = Organitzadors
        fields = ['empresa']


class NewFestaForm(ModelForm):
    nom = forms.CharField(label="Nom de la festa")
    data_inici = forms.DateTimeField(label="Data d'inici de la festa")
    data_fi = forms.DateTimeField(label="Data final de la festa")
    categoria = forms.CharField(label="Categoria")
    descripcio = forms.CharField(label="Descripcio")
    localitat = forms.CharField(label="Localitat")

    class Meta:
        model = Festes