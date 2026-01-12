from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'file', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nom dutilisateur')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'cou', 'poignee', 'cheville', 'available', 'materiaux', 'numero']