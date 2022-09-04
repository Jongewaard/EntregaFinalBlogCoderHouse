from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import *
from mensajeria.models import *
from django.contrib.auth.models import User


class UserSendingMessage(ModelForm):
    class Meta:
        model = Mensaje_privado
        fields = ["remitente","destinatario", "mensaje"]
        exclude = ["remitente", "destinatario"]

