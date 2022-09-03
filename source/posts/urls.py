from django.urls import path
from posts.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", index, name='home' ),
    path("login/", auth_login, name='login' ),
    path("logout/", LogoutView.as_view(template_name = "posts/logout.html"), name='logout' ),
    path("registrarse/", register, name='registrarse' ),
    path("edit_user/", modificar_usuario, name='editar_usuario'),
    path("view_post/", ver_post, name='ver_post'),
    path("create_post/", crear_post, name='crear_post')
]
