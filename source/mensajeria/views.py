from django.shortcuts import render, redirect
from mensajeria.models import *
from mensajeria.forms import *
from posts.models import *
from posts.forms import *


def ver_mensajes(request):
    contexto = {}
    if request.method == "GET":
        # Para la vista de mensajes creamos el formulario de envío de mensaje y lo agregamos al diccionario para el contexto
        form = UserSendingMessage()
        contexto = {"form":form}

        try: # para evitar un error por si no existe el avatar del usuario
            avatar = Avatar.objects.filter(user=request.user).first()
            dict_avatar = {"imagen":avatar.imagen.url}
        except:
            dict_avatar = {"imagen":""}
        contexto.update(dict_avatar)

        # enviamos de nuevo el usuario con el que nos mensajeamos por contexto
        usuario = User.objects.filter(id=request.GET.get('chat_con')).first()
        dict_usuarios = {"usr_remitente": usuario, "id_user_remitente":request.GET.get('chat_con')}
        contexto.update(dict_usuarios)

        mensajes = Mensaje_privado.objects.all()
        dict_mensajes = {"mensajes":mensajes, "user_logged":request.user.username}
        contexto.update(dict_mensajes)

        return render(request, "mensajeria/view_msgs.html", contexto )
    else:
        contexto = {}

        form = UserSendingMessage(request.POST)

        if form.is_valid(): #request.POST["id_post"]
            usuario = User.objects.filter(id=request.POST['destinatario_id']).first()
            instance = form.instance
            instance.remitente = request.user
            instance.destinatario = usuario
            instance.save()

            form = UserSendingMessage()
            contexto = {"form":form}

            try: # para evitar un error por si no existe el avatar del usuario
                avatar = Avatar.objects.filter(user=request.user).first()
                dict_avatar = {"imagen":avatar.imagen.url}
            except:
                dict_avatar = {"imagen":""}
            contexto.update(dict_avatar)

            # enviamos de nuevo el usuario con el que nos mensajeamos por contexto
            #usuario = User.objects.filter(id=request.GET.get('chat_con')).first()
            dict_usuarios = {"usr_remitente": usuario, "id_user_remitente":request.GET.get('chat_con')}
            contexto.update(dict_usuarios)

            mensajes = Mensaje_privado.objects.all()
            dict_mensajes = {"mensajes":mensajes, "user_logged":request.user.username}
            contexto.update(dict_mensajes)

        return render(request, "mensajeria/view_msgs.html", contexto )

def index_mensajes(request):
    contexto = {}
    # Acá la idea es listar los usuarios (excepto el logueado) para poder ver y escribir los mensajes que tenemos con..
    usuarios = User.objects.all()
    dict_of_users = {"users": usuarios}

    contexto.update(dict_of_users)
    return render(request, "mensajeria/see_users.html", contexto )