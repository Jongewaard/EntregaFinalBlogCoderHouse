from ast import Pass
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import *

class UserCustomCreationForm(UserCreationForm):
    username = CharField(label="Usuario")
    email = EmailField()
    password1 = CharField(label="Contraseña", widget=PasswordInput)
    password2 = CharField(label="Confirmar contraseña", widget=PasswordInput)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        help_texts = {k:"" for k in fields}

class CustomAuthenticationForm(AuthenticationForm):
    username = CharField(label="Usuario")
    password = CharField(label="Contraseña", widget=PasswordInput)
    class Meta:
        model = User
        fields = ["username","password"]
        #help_texts = {k:"" for k in fields}
        help_texts = {"username":"Usuario","password":"Contraseña"}

class UserEditForm(UserCreationForm):
    email = EmailField()
    password1 = CharField(label="Contraseña", widget=PasswordInput)
    password2 = CharField(label="Confirmar contraseña", widget=PasswordInput)
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
        help_texts = {k:"" for k in fields}