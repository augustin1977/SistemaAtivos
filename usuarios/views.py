from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario,Tipo
from log.models import Log
from django.shortcuts import redirect 
from hashlib import sha256
from usuarios.enviar_email import *
from usuarios.forms import *
import re
import string
import random
from django.http import Http404
from django.db.models import Q
import time
import json
from django.db.models import Count
from django.http import JsonResponse
from usuarios.autentica_usuario import *
def vazio(request):
    return redirect('/auth/login/') 
def login(request):
    # cria a view do login do usuário
    status=str(request.GET.get('status'))
    tipo=Tipo.objects.get(tipo="admin")
    administradores= Usuario.objects.filter(tipo=tipo).exclude(nome="System").order_by("nome")

    return render(request, "login.html", {'status':status,'administradores':administradores})

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
    if(usuario.tipo not in tipo): # verifica se o usuário é tipo admin
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
    usuario= Usuario.objects.filter(email=email)
    usuario_cadastro=Usuario.objects.get(id=request.session.get('usuario'))
    if len(usuario)>0:
        if (usuario[0].ativo==True):
            return redirect('/auth/cadastrar/?status=1') # retorna erro de usuario ja existente
        else:
            usuario[0].ativo=True
            usuario[0].primeiro_acesso=True
            usuario[0].senha=gera_senha(12)
            usuario[0].email=email
            usuario[0].chapa=chapa
            usuario[0].nome=nome
            usuario[0].tipo=tipo
            try:
                enviar_email(subject='Senha Sistema de gestão de ativos',
                             body=f"A senha provisória é {senha}",
                             recipients=[email,'gestaoativosma@gmail.com'])
                
                #send_mail(subject='Senha Sistema de gestão de ativos',message=f"A senha provisória é {senha}", from_email="gestaodeativos@outlook.com.br",recipient_list=[email,'gestaodeativos@outlook.com.br']) # antigo sistema de envio
            except Exception as e:
                # print(e)
                raise Http404("Impossivel enviar o e-mail com a senha, favor contactar o Administrador")
            usuario[0].save() # salva o objeto usuário no banco de dados
            log=Log(transacao='us',movimento='cd',usuario=usuario_cadastro,alteracao=f'O usuario {usuario_cadastro} cadastrou {usuario[0]} no sistema')
            log.save()
            return redirect('/listarUsuarios') # retorna sem  e com usuario

    if len(nome.strip())==0 :
        return redirect('/auth/cadastrar/?status=2') # retorna erro valor nulo
    
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.fullmatch(padrao, email):
        return redirect('/auth/cadastrar/?status=4') # email invalido
    try:    
        senhacod= sha256(senha.encode()).hexdigest() # recuperando senha e codificando num hash sha256
        usuario=Usuario(nome=nome, senha=senhacod, email=email, tipo=tipo, chapa=chapa, primeiro_acesso=primeiro_acesso,ativo=ativo) # cria um objeto usuário com as informações recebidas do fomulario
        try :
            usuario_cadastro=Usuario.objects.get(id=request.session.get('usuario'))
        except:
            usuario_cadastro=False
        try:
            conteudo_html = f"""<html>
                                <head></head>
                                <body>
                                    <h2>Olá {nome}!</h2>
                                    <p>Seu login foi criado no sistema de Gestão de Ativos do LPM.</p>
                                    <p>Os dados para login são:</p>
                                    <p>Seu nome de usuário: {email}</p>
                                    <p>Sua senha provisória: {senha}</p>
                                    <p>O link para acesso ao sistema é: <a href="http://gestaoativosma.ad.ipt.br/">gestaoativosma.ad.ipt.br </p>
                                    <p>Obrigado!</p>
                                    <p> Administrador do Sistema</p>
                                </body>
                                </html>"""
            conteudo_plain=f"A sua senha provisória é {senha}"
            enviar_email(subject='Senha Sistema de gestão de ativos',
                         body=conteudo_html,
                         recipients=[email,'gestaoativosma@gmail.com'])
            #send_mail(subject='Senha Sistema de gestão de ativos',message=conteudo_plain,html_message=conteudo_html, from_email="gestaodeativos@outlook.com.br",recipient_list=[email,'gestaodeativos@outlook.com.br']) 
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

    except Exception as e:
        # print(e)
        
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
        email=usuario[0].email
        nome=usuario[0].nome
        tipo=Tipo.objects.get(tipo="admin")
        administradores= Usuario.objects.filter(tipo=tipo)
        lista_admim=[]
        for administrador in administradores:
                lista_admim.append(administrador.email)
        conteudo_admin = f"""<html>
                            <head></head>
                            <body>
                                <h2>Notificação de recuperação de senha</h2>
                                <p>O usuário {nome} ({email}) solicitou uma nova senha.</p>
                            </body>
                            </html>"""
        conteudo_html = f"""<html>
                                <head></head>
                                <body>
                                    <h2>Olá {nome}!</h2>
                                    <p>Você solicitou envio de nova senha para sua conta.</p>
                                    <p>Os dados para login são:</p>
                                    <p>Seu nome de usuário: {email}</p>
                                    <p>Sua senha provisória: {novasenha}</p>
                                    <p>O link para acesso ao sistema é: <a href="http://gestaoativosma.ad.ipt.br/">gestaoativosma.ad.ipt.br </a></p>
                                    <p>Obrigado!</p>
                                    <p> Administrador do Sistema</p>
                                </body>
                                </html>"""
        try:
            
            enviar_email(subject='Senha Sistema de gestão de ativos',
                         body=conteudo_html,
                         recipients=[email,'gestaoativosma@gmail.com'])
            # print(lista_admim)
            time.sleep(2)
            enviar_email_background(
                subject='Notificação automática de recuperação de senha',
                body=conteudo_admin,
                recipients=lista_admim  # Lista de e-mails dos administradores
            )
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
@is_admin
def listarUsuarios(request):
    usuarios=Usuario.objects.filter(ativo=True).order_by('nome')
    return render(request, "listaUsuarios.html", {'usuarios':usuarios})
@is_admin
def listaUsuariosInativos(request):
    usuarios=Usuario.objects.filter(ativo=False).order_by('nome')
    return render(request, "listaUsuariosInativos.html", {'usuarios':usuarios})
@is_admin
def ativarUsuario(request):
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    user=Usuario.objects.get(id=request.GET.get('usuario'))
    user.ativo=True
    user.primeiro_acesso=True
    user.senha=gera_senha(12)
    log =Log(alteracao=f"O {usuario} reativou o usuario: {user} e criou uma nova senha para acesso ",usuario=usuario,transacao='us',movimento='ed')
    log.save() 
    conteudo_html = f"""<html>
                            <head></head>
                            <body>
                                <h2>Olá {user}!</h2>
                                <p>Foi solicitada uma nova senha para seu usuário pelo usuario administrador do sistema.</p>
                                <p>Os dados para login são:</p>
                                <p>Seu nome de usuário: {user.email}</p>
                                <p>Sua nova senha provisória: {user.senha}</p>
                                <p>O link do sistema é: <a href="http://gestaoativosma.ad.ipt.br/">gestaoativosma.ad.ipt.br </a> </p>
                                <p>Obrigado!</p>
                            </body>
                        </html>"""
    enviar_email_background(subject='Recuperação de senha Sistema de gestão de ativos',
                            body=conteudo_html,
                            recipients=[user.email,'gestaoativosma@gmail.com']) 
    user.save()
    return redirect('/listaUsuariosInativos/')
      
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
            usuarios=Usuario.objects.filter(ativo=True).order_by('nome')
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
    usuario_adm=Usuario.objects.get(id=request.session.get('usuario')) 
    tipo=Tipo.objects.get(tipo="admin")
    if(usuario_adm.tipo==tipo):
        usuarios=Usuario.objects.filter(ativo=True).order_by('nome')
        if request.method=="GET":
            id=request.GET.get('idUsuario')
            try:
                usuario_troca_senha=Usuario.objects.get(id=id,ativo=True)
            except:
                return render(request, "listaUsuarios.html", {'status':'1','usuarios':usuarios})# Usuario não cadastrado / Erro Geral
            
            novasenha=gera_senha(12)
            usuario_troca_senha.senha=sha256(novasenha.encode()).hexdigest()   
            usuario_troca_senha.primeiro_acesso=True
            
            try:
                conteudo_html = f"""<html>
                                <head></head>
                                <body>
                                    <h2>Olá {usuario_troca_senha}!</h2>
                                    <p>Foi solicitada uma nova senha para seu usuário pelo usuario administrador do sistema.</p>
                                    <p>Os dados para login são:</p>
                                    <p>Seu nome de usuário: {usuario_troca_senha.email}</p>
                                    <p>Sua nova senha provisória: {novasenha}</p>
                                    <p>O link do sistema é: <a href="http://gestaoativosma.ad.ipt.br/">gestaoativosma.ad.ipt.br </a> </p>
                                    <p>Obrigado!</p>
                                </body>
                                </html>"""
                enviar_email_background(subject='Recuperação de senha Sistema de gestão de ativos',
                         body=conteudo_html,
                         recipients=[usuario_troca_senha.email,'gestaoativosma@gmail.com'])              
       
                log=Log(transacao='us',movimento='ed',usuario=usuario_adm,
                        alteracao=f'O usuario {usuario_adm} recuperou a senha do {usuario_troca_senha} via sistema e eviou email para {usuario_troca_senha.email}')
                log.save()
                usuario_troca_senha.save()
                return render(request, "listaUsuarios.html", {'status':'51','usuarios':usuarios}) # troca de senha efetuada com sucesso  
            except Exception as e:
                # print(e)
                return render(request, "listaUsuarios.html", {'status':'2','usuarios':usuarios}) # Erro no envio do email
        
    return redirect('/auth/login/?status=0')
        
def maioresUsuarios(request):
    if not request.session.get("usuario"):
        return redirect("/auth/login/?status=2")
    usuario_adm=Usuario.objects.get(id=request.session.get('usuario')) 
    tipo=Tipo.objects.get(tipo="admin")
    if(usuario_adm.tipo==tipo):
        lista_usuarios={}
        registros_por_usuario = Log.objects.values('usuario__nome').annotate(num_registros=Count('id')).order_by('-num_registros')
        for item in registros_por_usuario:
            lista_usuarios[item['usuario__nome']]=item['num_registros']
        # print(lista_usuarios)   
        # print(registros_por_usuario )
        return render(request, "maioresusuarios.html", {'usuarios':registros_por_usuario})
    
    # JsonResponse(lista_usuarios,safe=False)
    return redirect(f'/equipamentos/?status=50')
def envia_mensagem_usuarios(request):
    if not request.session.get("usuario"):
        return redirect("/auth/login/?status=2")
    usuario_adm=Usuario.objects.get(id=request.session.get('usuario')) 
    tipo=Tipo.objects.get(tipo="admin")
    if(usuario_adm.tipo==tipo):
        if request.method=="GET":
            return render(request, "envio_email.html",{})
        
        todos=Usuario.objects.filter(ativo=True)
        emails=[]
        assunto="Teste"
        conteudo="Teste"
        
        for usuario in todos:
            emails.append(str(usuario.email))
        enviar_email(subject=assunto,body=conteudo,recipients=emails)
        #print(emails)    
    return redirect(f'/equipamentos/?status=0')