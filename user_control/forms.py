
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from user_control.models import Pessoa
from stonks.models import UserWallet

class SignUpForm(UserCreationForm):
    '''
        Form para cadastro de novos usuários.
    '''
    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Primeiro Nome'
        )

    email = forms.EmailField(
        max_length=254,
        help_text='E-mail'
        )

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password1', 'password2', )

    
    def save(self, commit=True):
        instance = super(SignUpForm, self).save(commit=False)
        instance.username = self.cleaned_data['email']
        instance.save()

        pessoa = Pessoa.objects.create(
            user=instance,
            first_name=self.cleaned_data['first_name'],
            email=self.cleaned_data['email']
        )
        UserWallet.objects.create(
            owner=pessoa,
            balance=0
        )
        return instance


class LoginForm(forms.Form):
    '''
        Form para login de usuários.
    '''

    email = forms.EmailField(
        max_length=254,
        help_text='E-mail'
        )

    password = forms.CharField(
        widget=forms.PasswordInput
        )

