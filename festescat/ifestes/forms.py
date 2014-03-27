from ifestes.models import Usuaris
from django.forms import ModelForm


class UserForm(ModelForm):
    class Meta:
        model = Usuaris
        exclude = ['user']
        fields = ['username', 'password', 'email']

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            return user


class LoginForm(ModelForm):
    class Meta:
        model = Usuaris
        exclude = ['user']
        fields = ['username', 'password']