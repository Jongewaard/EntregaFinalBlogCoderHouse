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
    estado = models.IntegerField(choices=STATUS, default=0)
    slug = models.SlugField(max_length=300, unique=True)

    f_creacion = models.DateTimeField(auto_now_add=True)
    f_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-f_creacion']

    def __str__(self):
        return self.titulo