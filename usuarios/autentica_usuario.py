from usuarios.models import * 
from django.shortcuts import redirect
def is_user(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            usuario = request.session.get('usuario')
        except:
            usuario=False
        if usuario:
            user= Usuario.objects.get(id=usuario)
            tipouser=Tipo.objects.get(tipo="user")
            tiposuperuser=Tipo.objects.get(tipo="superuser")
            tipoadmin=Tipo.objects.get(tipo="admin")
            if user.ativo==1 and (user.tipo==tipouser or user.tipo==tipoadmin or user.tipo==tiposuperuser):
                return view_func(request, *args, **kwargs)
           
        return redirect('/auth/login/?status=2')  # Redireciona para uma página de login ou qualquer outra página apropriada
    return wrapper
def is_superuser(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            usuario = request.session.get('usuario')
        except:
            usuario=False
        if usuario:
            user= Usuario.objects.get(id=usuario)
            tiposuperuser=Tipo.objects.get(tipo="superuser")
            tipoadmin=Tipo.objects.get(tipo="admin")
        if user.ativo==1 and (user.tipo==tipoadmin or user.tipo==tiposuperuser):
            return view_func(request, *args, **kwargs)
        return redirect("/equipamentos/?status=50")  # Redireciona para uma página de login ou qualquer outra página apropriada
    return wrapper

def is_admin(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            usuario = request.session.get('usuario')
        except:
            usuario=False
        if usuario:
            user= Usuario.objects.get(id=usuario)
            tipoadmin=Tipo.objects.get(tipo="admin")
        if user.ativo==1 and (user.tipo==tipoadmin ):
            return view_func(request, *args, **kwargs)
        return redirect("/equipamentos/?status=50")  # Redireciona para uma página de login ou qualquer outra página apropriada
    return wrapper