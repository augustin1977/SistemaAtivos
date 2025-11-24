from usuarios.models import * 
from django.shortcuts import redirect
def is_user(view_func):
    def wrapper(request, *args, **kwargs):
        usuario_id = request.session.get('usuario')
        if not usuario_id:
            return redirect("/equipamentos/?status=50")

        # Busca segura
        user = Usuario.objects.filter(id=usuario_id, ativo=1).select_related("tipo").first()
        if not user:
            return redirect("/equipamentos/?status=50")
        # Qualquer tipo válido
        tipos_validos = {"user", "admin", "superuser"}
        # Evita exceção caso não tenha tipo
        tipo_user = getattr(user.tipo, "tipo", None)
        if tipo_user in tipos_validos:
            return view_func(request, *args, **kwargs)  
        return redirect('/auth/login/?status=2')  # Redireciona para uma página de login ou qualquer outra página apropriada
    return wrapper
def is_superuser(view_func):
    def wrapper(request, *args, **kwargs):
        usuario_id = request.session.get('usuario')
        if not usuario_id:
            return redirect("/equipamentos/?status=50")
        # Busca segura
        user = Usuario.objects.filter(id=usuario_id, ativo=1).select_related("tipo").first()
        if not user:
            return redirect("/equipamentos/?status=50")
        # Qualquer tipo válido
        tipos_validos = {"admin", "superuser"}
        # Evita exceção caso não tenha tipo
        tipo_user = getattr(user.tipo, "tipo", None)
        if tipo_user in tipos_validos:
            return view_func(request, *args, **kwargs)  
        return redirect('/auth/login/?status=2')  # Redireciona para uma página de login ou qualquer outra página apropriada
    return wrapper

def is_admin(view_func):
    def wrapper(request, *args, **kwargs):
        usuario_id = request.session.get('usuario')
        if not usuario_id:
            return redirect("/equipamentos/?status=50")
        # Busca segura
        user = Usuario.objects.filter(id=usuario_id, ativo=1).select_related("tipo").first()
        if not user:
            return redirect("/equipamentos/?status=50")
        # Qualquer tipo válido
        tipos_validos = {"admin"}
        # Evita exceção caso não tenha tipo
        tipo_user = getattr(user.tipo, "tipo", None)
        if tipo_user in tipos_validos:
            return view_func(request, *args, **kwargs)  
        return redirect('/auth/login/?status=2')  # Redireciona para uma página de login ou qualquer outra página apropriada
    return wrapper