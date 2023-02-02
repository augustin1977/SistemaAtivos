from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario,Tipo
from log.models import Log
from django.shortcuts import redirect 
from hashlib import sha256
import re
def vazio(request):
    return redirect('/auth/cadastrar/') 
def login(request):
    # cria a view do login do usuário
    status=str(request.GET.get('status'))
    return render(request, "login.html", {'status':status})

def cadastrar(request):
    # cria a view do cadastro de usuaário
    status=str(request.GET.get('status'))
    return render(request, "cadastro.html", {'status':status})

def editar(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    usuario = Usuario.objects.get(id=request.session.get('usuario')) 
    if request.method=="GET":
        return render(request, "editar.html",{'usuario':usuario})
    senha_antiga=request.POST.get("senha_antiga")
    nova_senha=request.POST.get("senha_antiga")
    nome=request.POST.get("nome")
    email=request.POST.get("email")
    chapa=request.POST.get("chapa")
    senha_antiga=sha256(senha_antiga.encode()).hexdigest()
    if senha_antiga==usuario.senha:
        regex = "^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%<^&*?()])[a-zA-Z0-9!@#$%<^&*?()]{6,}" # verifica se tem ao menos uma letra, um numero, um simbolo e no minimo 6 caracteres 
        if  not (re.search(regex, nova_senha)):
            nova_senha=sha256(nova_senha.encode()).hexdigest()
            usuario.chapa=chapa
            usuario.nome=nome
            usuario.senha=nova_senha
            usuario.email=email
            usuario.save()
            return redirect('/auth/login/?status=0')
        else:
            return render(request, "editar.html",{'usuario':usuario,'status':3})

    return render(request, "editar.html",{'usuario':usuario,'status':1})
    


def valida_cadastro(request):
    # validar cadastro, falta implementar verificação de e-mail
    nome=request.POST.get('nome')
    email=request.POST.get('email')
    senha=request.POST.get('senha')
    chapa=request.POST.get("chapa")
    tipo=Tipo.objects.get(tipo="user")
    usuario= Usuario.objects.filter(email=email)
    
    if len(usuario)>0:
        return redirect('/auth/cadastrar/?status=1') # retorna erro de usuario ja existente
    usuario= Usuario.objects.filter(nome=nome)
    if len(usuario)>0:
        return redirect('/auth/cadastrar/?status=1') # retorna erro de usuario ja existente
    if len(nome.strip())==0 or len(email.strip())==0 :
        return redirect('/auth/cadastrar/?status=2') # retorna erro valor nulo
    if len(usuario)>0:
        return redirect('/auth/cadastrar/?status=2') # chapa nula
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'    
    if not(re.search(regex,email)): 
        return redirect('/auth/cadastrar/?status=4') # email invalido   
    
    regex = "^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%<^&*?()])[a-zA-Z0-9!@#$%<^&*?()]{6,}" # verifica se tem ao menos uma letra, um numero, um simbolo e no minimo 6 caracteres 
    if  not (re.search(regex, senha)) :
        return redirect('/auth/cadastrar/?status=3') # Senha invalida
    try:
        senha= sha256(senha.encode()).hexdigest() # recuperando senha e codificando num hash sha256
        usuario=Usuario(nome=nome, senha=senha, email=email, tipo=tipo, chapa=chapa) # cria um objeto usuário com as informações recebidas do fomulario
        usuario.save() # salva o objeto usuário no banco de dados
        log=Log(transacao='us',movimento='cd',usuario=usuario,alteracao=f'{usuario} se cadastrou no sistema')
        log.save()
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
        print(f"{usuario[0].nome} logou no sistema")
        log=Log(transacao='us',movimento='lo',usuario=Usuario.objects.get(id=usuario[0].id),alteracao=f'{usuario[0]} logou no sistema')
        log.save()
        return redirect(f'/equipamentos/?status=0')
    
def sair(request):
    request.session.flush() # sair do usuário
    return redirect('/auth/login')
