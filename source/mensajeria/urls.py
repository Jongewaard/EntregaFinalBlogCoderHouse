from django.urls import path
from posts.views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from mensajeria.views import *


urlpatterns = [
    path("indx_msgs/", index_mensajes, name='indx_msgs' ),
    path("ver_mensajes/", ver_mensajes, name='ver_mensajes' ),
]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)