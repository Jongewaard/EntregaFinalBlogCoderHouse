from django.db import models
from django.contrib.auth.models import User


STATUS = (
    (0,"Proyecto"),
    (1,"Publicado")
)

class Post(models.Model):
    titulo = models.CharField(max_length=300, unique=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    contenido = models.TextField()
    estado = models.IntegerField(choices=STATUS, default=1)
    slug = models.SlugField(max_length=300, unique=True)

    f_creacion = models.DateTimeField(auto_now_add=True)
    f_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-f_creacion']

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    related_post = models.IntegerField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=150)

    f_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['f_creacion']

    def __str__(self):
        return f"{self.autor}: {self.comentario}"

class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="avatares", null=True, blank=True)