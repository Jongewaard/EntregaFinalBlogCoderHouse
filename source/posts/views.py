from django.shortcuts import render, redirect
from posts.models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from posts.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
    try:
        avatar = Avatar.objects.filter(user=request.user).first()
    except:
        pass # nomas para evitar el error de que haya un usuario sin imagen, o si entran sin loguearse
    try:# Podría capturar mas elegantemente el error, pero esta gronchada funciona xd
        dict_avatar = {"imagen":avatar.imagen.url}
    except:
        dict_avatar = {"imagen":""}
    contexto = {}
    contexto.update(dict_avatar)
    return render(request, "posts/index.html", contexto)

def auth_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data = request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('password')
            user = authenticate(username=usuario, password=contrasenia)
            if user is not None:
                login(request, user)
                return redirect("home")#login exitoso
            else:
                contexto = {
                    'error':'Error, formulario inválido',
                    'form': CustomAuthenticationForm()
                    }
                return render(request,"posts/login.html",contexto)#login con errores, o datos incorrectos
        else:
            contexto = {
            'error':'Error, datos incorrectos',
            'form': CustomAuthenticationForm()
            }
            return render(request,"posts/login.html",contexto)#login con errores, o datos incorrectos
    form = CustomAuthenticationForm()
    return render(request, "posts/login.html",{'form':form} )

def register(request):
    if request.method == 'POST':
        form = UserCustomCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            return render(request,"posts/index.html")#Usuario creado
        form = UserCustomCreationForm()
        return render(request,"posts/register.html", {"form":form,"error": "Error al crear usuario, verifique fortaleza de contraseña, un correo adecuado y un usuario válido"})#Error al crear usuario

    else:
        form = UserCustomCreationForm()
        return render(request, "posts/register.html", {"form":form} )

@login_required
def modificar_usuario(request):
    if request.method == "GET":
        avatar = Avatar.objects.filter(user=request.user).first()
        try:# Podría capturar mas elegantemente el error, pero esta gronchada funciona xd
            dict_avatar = {"imagen":avatar.imagen.url}
        except:
            dict_avatar = {"imagen":""}
        form = UserEditForm(initial={"email":request.user.email})
        img_form = AvatarForm()
        contexto = {
            "form":form,
            "image_form":img_form
        }
        contexto.update(dict_avatar)
        return render(request, 'posts/user_update.html',contexto)
    else:

        try:
            if request.POST["cargando_imagen"]:
                form = AvatarForm(request.POST, request.FILES)
                if form.is_valid():
                    print(f"el formulario es valido!")
                    data = form.cleaned_data
                    usuario = User.objects.filter(username=request.user.username).first()
                    avatar = Avatar(user=usuario,imagen=data["imagen"])
                    Avatar.objects.filter(user=request.user).delete()
                    avatar.save()
                return redirect("ver_post")
        except:
            pass
        form = UserEditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            usuario = request.user
            usuario.email = data["email"]
            usuario.password1 = data["password1"]
            usuario.password2 = data["password2"]
            usuario.save()
        return redirect("home")

def ver_post(request):
    dict_of_search = {}
    if request.method == "GET":
        try:
            avatar = Avatar.objects.filter(user=request.user).first()
            dict_avatar = {"imagen":avatar.imagen.url}
            #avatar = Avatar.objects.filter(user=request.user).order_by('-id')
        except:
            dict_avatar = {"imagen":""} # esto es para evitar un crash si no hay usuario logueado

        avatares = Avatar.objects.all()
        dict_avatares = {"imagenes":avatares}
        try:
            listado_posteos = Post.objects.filter(contenido__contains=request.GET.get('cont_busqueda'))
            dict_of_search = {
                "busqueda_anterior": request.GET.get('cont_busqueda'),
                "largo_busqueda": len(listado_posteos)
                }
        except:
            listado_posteos = Post.objects.all()
        listado_comentarios = Comentario.objects.all()
        form = UserCommentPost()
        contexto = {
            "post_lists": listado_posteos,
            "form": form,
            "comments":listado_comentarios
            }
        contexto.update(dict_avatar)
        contexto.update(dict_avatares)
        contexto.update(dict_of_search)
        return render(request, "posts/posts.html", contexto)
    else:
        form = UserCommentPost(request.POST)

        # esto es una gronchada xd
        try:
            if request.POST["id_comentario_borrar"]:
                Comentario.objects.filter(id=request.POST["id_comentario_borrar"]).update(comentario='--deleted--')
            return redirect("ver_post")
        except:
            pass

        if form.is_valid():
            data = form.cleaned_data
            instance = form.instance
            instance.autor = request.user
            instance.related_post = request.POST["id_post"]
            instance.save()
        return redirect("ver_post")

@login_required
def crear_post(request):
    if request.method == "GET":
        form = UserCreationPost()
        return render(request, "posts/create_post.html", {"form":form} )
    else:
        form = UserCreationPost(request.POST)
        if form.is_valid():
            instance = form.instance
            instance.autor = request.user
            instance.save()

        return redirect("ver_post")

@login_required
def edit_post(request):
    if request.method == "GET":
        posteo_a_editar = Post.objects.filter(id=request.GET.get("id_post")).values()
        dict_of_initial = {
            "titulo":posteo_a_editar[0]["titulo"],
            "contenido":posteo_a_editar[0]["contenido"],
            "estado":posteo_a_editar[0]["estado"],
            "slug":posteo_a_editar[0]["slug"],
        }
        form = UserCreationPost(initial=dict_of_initial)
        return render(request, "posts/edit_post.html", {"form":form, "id_post_mod": request.GET.get("id_post") } )
    else:
        posteo_a_editar = Post.objects.filter(id=request.GET.get("id_post")).values()
        Post.objects.filter(id=request.POST["id_post"]).update(titulo=request.POST["titulo"],contenido=request.POST["contenido"],estado=request.POST["estado"])

        return redirect("ver_post")

def ver_about(request):
    try:# Podría capturar mas elegantemente el error, pero esta gronchada funciona xd
        avatar = Avatar.objects.filter(user=request.user).first()
        contexto = {"imagen":avatar.imagen.url}
    except:
        contexto = {"imagen":""}
    return render(request, "posts/about.html",contexto )


