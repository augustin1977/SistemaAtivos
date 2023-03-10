from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario,Tipo
from log.models import Log
from django.shortcuts import redirect 
from hashlib import sha256
from django.core.mail import send_mail
import re
import string
import random
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
    nova_senha=request.POST.get("senha_nova")
    nova_senha2=request.POST.get("senha_nova2")

    nome=request.POST.get("nome")
    email=request.POST.get("email")
    chapa=request.POST.get("chapa")

    if nova_senha!= nova_senha2:
        return render(request, "editar.html",{'usuario':usuario,'status':5})
    senha_antiga=sha256(senha_antiga.encode()).hexdigest()
    
    if senha_antiga==usuario.senha:
        #regex = "^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%<^&*?()])[a-zA-Z0-9!@#$%<^&*?()]{6,}" # verifica se tem ao menos uma letra, um numero, um simbolo e no minimo 6 caracteres 
        if  True :#(re.search(regex, nova_senha)):
            nova_senha=sha256(nova_senha.encode()).hexdigest()
            usuario.chapa=chapa
            usuario.nome=nome
            usuario.senha=nova_senha
            usuario.email=email
            usuario.primeiro_acesso=False
            usuario.save()
            log=Log(transacao='us',movimento='ed',usuario=usuario,alteracao=f'{usuario} Alterou a senha de acesso')
            log.save()
            return redirect(f'/equipamentos/')
        else:
            return render(request, "editar.html",{'usuario':usuario,'status':3})
    return render(request, "editar.html",{'usuario':usuario,'status':1})
    


def valida_cadastro(request):
    # validar cadastro, falta implementar verificação de e-mail
    nome=request.POST.get('nome')
    email=request.POST.get('email')
    senha=gera_senha(12)
    chapa=request.POST.get("chapa")
    tipo=Tipo.objects.get(tipo="user")
    primeiro_acesso=True
    usuario= Usuario.objects.filter(email=email)
    
    if len(usuario)>0:
        return redirect('/auth/cadastrar/?status=1') # retorna erro de usuario ja existente

    if len(nome.strip())==0 :
        return redirect('/auth/cadastrar/?status=2') # retorna erro valor nulo
    
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.fullmatch(padrao, email):
        return redirect('/auth/cadastrar/?status=4') # email invalido


    try:    
        senhacod= sha256(senha.encode()).hexdigest() # recuperando senha e codificando num hash sha256
        print("cria Senha")
        usuario=Usuario(nome=nome, senha=senhacod, email=email, tipo=tipo, chapa=chapa, primeiro_acesso=primeiro_acesso) # cria um objeto usuário com as informações recebidas do fomulario
        log=Log(transacao='us',movimento='cd',usuario=usuario,alteracao=f'O usuario {usuario} se cadastrou no sistema')
        send_mail(subject='Senha Sistema de gestão de ativos',message=f"A senha provisória {senha}", from_email="gestaodeativos@outlook.com.br",recipient_list=[email,'ericaugustin@ipt.br']) 
        usuario.save() # salva o objeto usuário no banco de dados
        log.save()
        return redirect('/auth/login/?status=0') # retorna sem erro
    except:
        return redirect('/auth/cadastrar/?status=99') # retorna erro geral de gravação no banco de dados
  
    return HttpResponse("Erro na pagina de cadastro - View")

def validar_login(request):
    # validar o login feito na pagina de login
    email=request.POST.get('email')
    senha=request.POST.get('senha')
    #primeiro_acesso=False
    senha=sha256(senha.encode()).hexdigest()
    usuario=Usuario.objects.filter(email=email).filter(senha=senha)
    
    if len(usuario)==0:
        return redirect('/auth/login/?status=1')
    else:
        request.session['usuario']= usuario[0].id
        print(f"{usuario[0].nome} logou no sistema")
        log=Log(transacao='us',movimento='lo',usuario=Usuario.objects.get(id=usuario[0].id),alteracao=f'{usuario[0]} logou no sistema')
        log.save()
        if usuario[0].primeiro_acesso==True:
            return redirect('/auth/editar/?status=1')
        return redirect(f'/equipamentos/?status=0')

def esqueci_senha(request):
    
    if request.method=="GET":
        status=request.GET.get('status')
        return render(request, "esqueci_senha.html", {'status':status})
    else:
        email= request.POST.get('email')
        usuario=Usuario.objects.filter(email=email)
        if len(usuario)==0:
            return redirect('/auth/esqueci_senha/?status=1') # Usuario não cadastrado
        novasenha=gera_senha(12)
        usuario[0].senha=sha256(novasenha.encode()).hexdigest()   
        usuario[0].primeiro_acesso=True
        try:
            send_mail(subject='Recuperação de Senha Sistema de gestão de ativos',message=f"A sua nova senha é {novasenha}",
            from_email="gestaodeativos@outlook.com.br",recipient_list=[usuario[0].email,'ericaugustin@ipt.br'])  
        except:
            return redirect('/auth/esqueci_senha/?status=2') # Falha no envio
        
        log=Log(transacao='us',movimento='ed',usuario=usuario[0],alteracao=f'O usuario {usuario[0]} recuperou a senha via e-mail - email enviado para {usuario[0].email}')
        log.save()
        usuario[0].save()
        
        return redirect('/auth/login/?status=51') # nova senha enviada por email com sucesso
def sair(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    log=Log(transacao='us',movimento='lf',usuario=usuario,alteracao=f'{usuario} saiu do sistema')
    log.save()
    request.session.flush() # sair do usuário
    return redirect('/auth/login')




def gera_senha(tamanho):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(random.choice(caracteres) for i in range(tamanho))
    return senha