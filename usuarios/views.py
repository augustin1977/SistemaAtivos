from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario,Tipo
from log.models import Log
from django.shortcuts import redirect 
from hashlib import sha256
from django.core.mail import send_mail
from usuarios.forms import *
import re
import string
import random
from django.http import Http404
from django.db.models import Q
def vazio(request):
    return redirect('/auth/login/') 
def login(request):
    # cria a view do login do usuário
    status=str(request.GET.get('status'))
    return render(request, "login.html", {'status':status})

def cadastrar(request):
    # cria a view do cadastro de usuaário
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    status=str(request.GET.get('status'))

    # ### Bloco de bloqueio de usuario para acesso ###   
    # tipo1=Q(tipo="superuser")
    # tipo2=Q(tipo='especialuser')
    tipo3=Q(tipo='admin')
    tipo=Tipo.objects.filter(tipo3)
    usuario= Usuario.objects.get(id=request.session.get('usuario'))
    if(usuario.tipo not in tipo): # verifica se o usuário é tipo especial
        return redirect(f'/equipamentos/?status=50') # se não for redireciona para pagina de acesso recusado
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
    ativo=True
    usuario= Usuario.objects.filter(email=email,ativo=True)
    
    if len(usuario)>0:
        if (usuario[0].ativo==True):
            return redirect('/auth/cadastrar/?status=1') # retorna erro de usuario ja existente
        else:
            usuario[0].ativo=True
            usuario[0].primeiro_acesso=True
            usuario[0].senha=gera_senha(12)
            usuario[0].email=email
            usuario[0].chapa=chapa
            try :
                usuario_cadastro=Usuario.objects.get(id=request.session.get('usuario'))
            except:
                usuario_cadastro=False

            try:
                send_mail(subject='Senha Sistema de gestão de ativos',message=f"A senha provisória é {senha}", from_email="gestaodeativos@outlook.com.br",recipient_list=[email,'gestaodeativos@outlook.com.br']) 
            except:
                raise Http404("Impossivel enviar o e-mail com a senha, favor contactar o Administrador")
            usuario[0].save() # salva o objeto usuário no banco de dados
            if usuario_cadastro:
                log=Log(transacao='us',movimento='cd',usuario=usuario_cadastro,alteracao=f'O usuario {usuario_cadastro} cadastrou {usuario[0]} no sistema')
            else:
                log=Log(transacao='us',movimento='cd',usuario=usuario[0],alteracao=f'O usuario {usuario[0]} se cadastrou no sistema')
            log.save()
            

    if len(nome.strip())==0 :
        return redirect('/auth/cadastrar/?status=2') # retorna erro valor nulo
    
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.fullmatch(padrao, email):
        return redirect('/auth/cadastrar/?status=4') # email invalido
    try:    
        senhacod= sha256(senha.encode()).hexdigest() # recuperando senha e codificando num hash sha256
        ##print("cria Senha")

        usuario=Usuario(nome=nome, senha=senhacod, email=email, tipo=tipo, chapa=chapa, primeiro_acesso=primeiro_acesso,ativo=ativo) # cria um objeto usuário com as informações recebidas do fomulario
        try :
            usuario_cadastro=Usuario.objects.get(id=request.session.get('usuario'))
        except:
            usuario_cadastro=False

        try:
            send_mail(subject='Senha Sistema de gestão de ativos',message=f"A sua senha provisória é {senha}", from_email="gestaodeativos@outlook.com.br",recipient_list=[email,'gestaodeativos@outlook.com.br']) 
        except:
            raise Http404("Impossivel enviar o e-mail com a senha, favor contactar o Administrador")
        usuario.save() # salva o objeto usuário no banco de dados
        if usuario_cadastro:
            log=Log(transacao='us',movimento='cd',usuario=usuario_cadastro,alteracao=f'O usuario {usuario_cadastro} cadastrou {usuario} no sistema')
        else:
            log=Log(transacao='us',movimento='cd',usuario=usuario,alteracao=f'O usuario {usuario} se cadastrou no sistema')
        log.save()
        ##print("usuario criado")
        if usuario_cadastro:
            return redirect('/listarUsuarios') # retorna sem  e com usuario
        
        else:
            return redirect('/auth/login/?status=0') # retorna sem erro e sem usuario

    except:
        return redirect('/auth/cadastrar/?status=99') # retorna erro geral de gravação no banco de dados
  
    return HttpResponse("Erro na pagina de cadastro - View")

def validar_login(request):
    # validar o login feito na pagina de login
    email=request.POST.get('email')
    senha=request.POST.get('senha')
    #primeiro_acesso=False
    senha=sha256(senha.encode()).hexdigest()
    usuario=Usuario.objects.filter(email=email).filter(senha=senha).filter(ativo=True)
    
    if len(usuario)==0:
        return redirect('/auth/login/?status=1')
    else:
        request.session['usuario']= usuario[0].id
        ##print(f"{usuario[0].nome} logou no sistema")
        #log=Log(transacao='us',movimento='lo',usuario=Usuario.objects.get(id=usuario[0].id),alteracao=f'{usuario[0]} logou no sistema')
        #log.save()
        if usuario[0].primeiro_acesso==True:
            return redirect('/auth/editar/?status=1')
        return redirect(f'/equipamentos/?status=0')

def esqueci_senha(request):
    
    if request.method=="GET":
        status=request.GET.get('status')
        return render(request, "esqueci_senha.html", {'status':status})
    else:
        email= request.POST.get('email')
        usuario=Usuario.objects.filter(email=email,ativo=True)
        if len(usuario)==0:
            return redirect('/auth/esqueci_senha/?status=1') # Usuario não cadastrado
        novasenha=gera_senha(12)
        usuario[0].senha=sha256(novasenha.encode()).hexdigest()   
        usuario[0].primeiro_acesso=True
        try:
            send_mail(subject='Recuperação de Senha Sistema de gestão de ativos',message=f"A sua nova senha é {novasenha}",
            from_email="gestaodeativos@outlook.com.br",recipient_list=[usuario[0].email,'gestaodeativos@outlook.com.br'])  
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
    #log=Log(transacao='us',movimento='lf',usuario=usuario,alteracao=f'{usuario} saiu do sistema')
    #log.save()
    request.session.flush() # sair do usuário
    return redirect('/auth/login')

def gera_senha(tamanho):
    caracteres = string.ascii_letters + string.digits + string.punctuation + string.ascii_letters
    senha = ''.join(random.choice(caracteres) for i in range(tamanho-1))
    senha=random.choice(string.ascii_uppercase)+senha
    return senha

def listarUsuarios(request):
    
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=1')
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    tipo=Tipo.objects.get(tipo="admin")
    if(usuario.tipo==tipo):
        usuarios=Usuario.objects.filter(ativo=True).order_by('nome')
        return render(request, "listaUsuarios.html", {'usuarios':usuarios})
    else:
        return redirect(f'/equipamentos/?status=50')

def exibirUsuario(request):
    if not request.session.get("usuario"):
        return redirect("/auth/login/?status=2")
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    tipo=Tipo.objects.get(tipo="admin")
    user=Usuario.objects.get(id=request.GET.get('usuario'))
    ##print(usuario.nome,usuario.tipo,usuario.id)
    if not usuario:
        return redirect('/auth/login/?status=1')
    elif(usuario.tipo==tipo):
        return render(request, "exibirUsuario.html", {'usuario':user})
    else:
        return redirect(f'/equipamentos/?status=50')

def editarUsuario(request):
    
    
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=1')
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    tipo=Tipo.objects.get(tipo="admin")
    if(usuario.tipo==tipo):
        if request.method=="GET":
            user=Usuario.objects.get(id=request.GET.get('usuario'))
            ##print(user)
            form=EditaUsuarioForm(instance=user)
            return render(request, "editarUsuario.html", {'form':form})
        elif request.method=="POST":
            details = EditaUsuarioForm(request.POST)
            if details.is_valid():
                user=Usuario.objects.get(id=details.cleaned_data['id'])
                listaCampos=['nome','chapa','email','tipo','primeiro_acesso']
                alteracao=False
                for campo in listaCampos:
                    alterado=Log.foiAlterado(transacao='us',objeto=user,atributo=campo,valor=details.cleaned_data[campo],usuario=usuario) 
                    if alterado:
                        setattr(user,campo,details.cleaned_data[campo])
                    alteracao|=alterado
                if alteracao:
                    user.save() 
            usuarios=Usuario.objects.filter(ativo=True)
            return render(request, "listaUsuarios.html", {'usuarios':usuarios})
        else:
            return redirect(f'/equipamentos/?status=99')
    else:
        return redirect(f'/equipamentos/?status=50')
    
def excluirUsuario(request):
    

    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=1')
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    tipo=Tipo.objects.get(tipo="admin")
    if(usuario.tipo==tipo):
        if request.method=="GET":
            user=Usuario.objects.get(id=request.GET.get("usuario"))
            return render(request, "excluirUsuario.html", {'usuario':user})
        elif request.method=="POST":
            user=Usuario.objects.get(id=request.POST.get('id'))
            user.ativo=False
            user.save()
            Log.exclusao(objeto=user,usuario=usuario,transacao='us')            
            return redirect('/listarUsuarios/')
    return  redirect(f'/equipamentos/?status=50')
# Implementado e não testado

def trocasenha(request):
    if not request.session.get("usuario"):
        return redirect("/auth/login/?status=2")
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    tipo=Tipo.objects.get(tipo="admin")
    if(usuario.tipo==tipo):
        usuarios=Usuario.objects.filter(ativo=True).order_by('nome')
        if request.method=="GET":
            id= request.GET.get('idUsuario')
            try:
                usuario_troca_senha=Usuario.objects.get(id=id,ativo=True)
            except:
                return render(request, "listaUsuarios.html", {'status':'1','usuarios':usuarios})# Usuario não cadastrado / Erro Geral
            novasenha=gera_senha(12)
            usuario_troca_senha.senha=sha256(novasenha.encode()).hexdigest()   
            usuario_troca_senha.primeiro_acesso=True
            try:
                send_mail(subject='Recuperação de Senha Sistema de gestão de ativos',message=f"A sua nova senha é {novasenha}",
                from_email="gestaodeativos@outlook.com.br",recipient_list=[usuario_troca_senha.email,'gestaodeativos@outlook.com.br'])
                usuario_adm=request.session['usuario']
                log=Log(transacao='us',movimento='ed',usuario=usuario_adm,
                        alteracao=f'O usuario {usuario_adm} recuperou a senha do {usuario_troca_senha} via sistema e eviou email para {usuario_troca_senha.email}')
                log.save()
                usuario_troca_senha.save()
                return render(request, "listaUsuarios.html", {'status':'51','usuarios':usuarios}) # troca de senha efetuada com sucesso  
            except:
                return render(request, "listaUsuarios.html", {'status':'2','usuarios':usuarios}) # Erro no envio do email
        
    return redirect('/auth/login/?status=0')
        
        
    