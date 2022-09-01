from msilib.schema import ListView
from turtle import isvisible
from django.shortcuts import render, redirect
from posts.models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from posts.forms import UserCustomCreationForm, CustomAuthenticationForm, UserEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# con @login_required se protege cualquier vista para ser necesario estar logueado
# esto es para vistas basadas en funciones

'''class Posteos(LoginRequiredMixin,ListView):
    # @login_required es para vistas basadas en CLASES 1:38:30 video de la clase 23
    pass'''


def index(request):
    listado_posteos = Post.objects.all()
    return render(request, "posts/index.html", {"post_lists": listado_posteos})


def auth_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data = request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('password')
            user = authenticate(username=usuario, password=contrasenia)
            if user is not None:
                login(request, user)
                return render(request,"posts/index.html")#login exitoso
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
            #return redirect('home')
            return render(request,"posts/index.html")#Usuario creado
    else:
        form = UserCustomCreationForm()
        return render(request, "posts/register.html", {"form":form} )

@login_required
def modificar_usuario(request):
    if request.method == "GET":
        form = UserEditForm(initial={"email":request.user.email})
        return render(request, 'posts/user_update.html',{"form":form})
    else:
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
    listado_posteos = Post.objects.all()
    return render(request, "posts/posts.html", {"post_lists": listado_posteos})