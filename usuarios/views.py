from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario,Tipos,Familia
from django.shortcuts import redirect 
from hashlib import sha256
import re
def login(request):
    # cria a view do login do usuário
    status=str(request.GET.get('status'))
    return render(request, "login.html", {'status':status})

def cadastrar(request):
    # cria a view do cadastro de usuaário
    status=str(request.GET.get('status'))
    return render(request, "cadastro.html", {'status':status})

def editar(request):
    # Cria a view que edita o cadastro do usuário, ainda não implementado
    return render(request, "editar.html")

def valida_cadastro(request):
    # validar cadastro, falta implementar verificação de e-mail
    nome=request.POST.get('nome')
    email=request.POST.get('email')
    senha=request.POST.get('senha')
    tipo=Tipos.objects.get(tipo="user")
    usuario= Usuario.objects.filter(email=email)
    familia=Familia.objects.get(nomeFamilia="Sem_Familia")
    if len(usuario)>0:
        return redirect('/auth/cadastrar/?status=1') # retorna erro de usuario ja existente
    usuario= Usuario.objects.filter(nome=nome)
    if len(usuario)>0:
        return redirect('/auth/cadastrar/?status=1') # retorna erro de usuario ja existente
    if len(nome.strip())==0 or len(email.strip())==0 :
        return redirect('/auth/cadastrar/?status=2') # retorna erro valor nulo
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'    
    if not(re.search(regex,email)): 
        return redirect('/auth/cadastrar/?status=4') # email invalido   
    
    regex = "^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%<^&*?()])[a-zA-Z0-9!@#$%<^&*?()]{6,}" # verifica se tem ao menos uma letra, um numero, um simbolo e no minimo 6 caracteres 
    if  not (re.search(regex, senha)) :
        return redirect('/auth/cadastrar/?status=3') # Senha invalida
    try:
        senha= sha256(senha.encode()).hexdigest() # recuperando senha e codificando num hash sha256
        usuario=Usuario(nome=nome, senha=senha, email=email, tipo=tipo, nomeFamilia=familia) # cria um objeto usuário com as informações recebidas do fomulario
        usuario.save() # salva o objeto usuário no banco de dados
        return redirect('/auth/login/?status=0') # retorna sem erro
    except:
        return redirect('/auth/cadastrar/?status=99') # retorna erro geral de gravação no banco de dados
  
    return HttpResponse("Erro na pagina de cadastro - View")

def validar_login(request):
    # validar o login feito na pagina de login
    email=request.POST.get('email')
    senha=request.POST.get('senha')
    senha=sha256(senha.encode()).hexdigest()
    usuario=Usuario.objects.filter(email=email).filter(senha=senha)
    
    if len(usuario)==0:
        return redirect('/auth/login/?status=1')
    else:
        request.session['usuario']= usuario[0].id
        return redirect(f'/receita/home/')
    
def sair(request):
    request.session.flush() # sair do usuário
    return redirect('/auth/login')
