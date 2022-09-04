from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Mensaje_privado(models.Model):
    remitente = models.CharField(max_length=150, default="")
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=150, default="")
    f_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['f_creacion']

    def __str__(self):
        return f"{self.remitente} -> {self.destinatario} -> {self.mensaje}"