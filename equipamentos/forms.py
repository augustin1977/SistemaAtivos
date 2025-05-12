# -*- coding: utf-8 -*-
from django import forms
from django.forms import *
from .models import *
from djmoney.forms.fields import MoneyField,MoneyWidget
from cadastro_equipamentos.settings import TIME_ZONE
import datetime
import pytz
import os

class CustomMoney(MoneyField):
    """Cria padrão para exibição de valores em dinheiro, subistituindo . por ,"""
    def clean(self, value):
        value[0] = value[0].replace(',', '.')
        value= super().clean(value)

        return value

class localFormCadastro(ModelForm):
    """ Cria formulário de cadastro de local de instalação"""
    class Meta:
        model = Local_instalacao
        fields = '__all__'
        widgets = {
            'laboratorio': TextInput (attrs={'class': "form-control",'placeholder':'LPM'}),
            'predio': TextInput (attrs={'class': "form-control",'placeholder':'1'}),
            'piso':TextInput (attrs={'class': "form-control", 'placeholder':'Térreo'}),
            'sala':TextInput (attrs={'class': "form-control",'placeholder':'Sala 01'}),
            'armario':TextInput (attrs={'class': "form-control",'placeholder':'Armário'}),
            'prateleira':TextInput (attrs={'class': "form-control",'placeholder':'Prateleira 1'}),
            'apelido_local':TextInput (attrs={'class': "form-control",'label': "Detalhes",'placeholder':'complemento'}),

        }

class localFormEditar(ModelForm):
    """Cria formaulario de edição do local de instalação"""
    id=CharField(label="",widget=HiddenInput())
    class Meta:
        model = Local_instalacao
        fields = '__all__'
        widgets = {
            'id': HiddenInput(),
            'laboratorio': TextInput (attrs={'class': "form-control"}),
            'predio': TextInput (attrs={'class': "form-control"}),
            'piso':TextInput (attrs={'class': "form-control"}),
            'sala':TextInput (attrs={'class': "form-control"}),
            'armario':TextInput (attrs={'class': "form-control"}),
            'prateleira':TextInput (attrs={'class': "form-control"}),
            'apelido_local':TextInput (attrs={'class': "form-control",'label': "Detalhes"}),

        }

class  localFormlista(ModelForm):
    """Cria lista de locais de instalação"""
    ListaLocais = modelformset_factory(Local_instalacao, fields=('__all__'))
    class Meta:
        model = Local_instalacao
        fields = '__all__'

class equipamentoEditarForm(Form):
    """Cria formulario de edição do cadastro dos equipamentos"""
    id=CharField(label="",widget=HiddenInput())
    nome_equipamento=CharField(widget= TextInput(attrs={'class': "form-control"}))
    modelo=CharField(widget= TextInput(attrs={'class': "form-control"}))
    codigo = CharField(widget=TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    fabricante=ModelChoiceField(queryset=Fabricante.objects.all() ,widget=Select (attrs={'class': "form-control"}))
    local=ModelChoiceField(queryset=Local_instalacao.objects.all(),widget=Select(attrs={'class': "form-control"}))
    tipo_equipamento=ModelChoiceField(queryset= Tipo_equipamento.objects.all(),widget=Select(attrs={'class': "form-control"}))
    data_compra=DateTimeField(widget=DateInput( attrs={'class': 'form-control'}),error_messages={'invalid': 'Por favor, insira uma data válida.'} )
    data_ultima_calibracao=DateTimeField(required=False,widget=DateInput( attrs={'class': 'form-control'}),error_messages={'invalid': 'Por favor, insira uma data válida.'} )
    patrimonio=CharField(widget= TextInput(attrs={'class': "form-control"}))
    # material_consumo=ModelMultipleChoiceField(required=False,blank=True,queryset= Material_consumo.objects.all(),widget=SelectMultiple(attrs={'class': "form-control"}))
    usuario=CharField(label="",widget=HiddenInput())
    custo_aquisição=CustomMoney(default_currency='BRL',required=False,widget= MoneyWidget(attrs={'class': "form-control"}))
    responsavel=CharField(widget= TextInput(attrs={'class': "form-control"}))
    potencia_eletrica=CharField(required=False,widget= TextInput(attrs={'class': "form-control"}))
    nacionalidade=CharField(required=False,widget= TextInput(attrs={'class': "form-control"}))
    tensao_eletrica=CharField(required=False,widget= TextInput(attrs={'class': "form-control"}))
    projeto_compra=CharField(required=False,widget= TextInput(attrs={'class': "form-control"}))
    especificacao=CharField(required=False,widget= Textarea(attrs={'class': "form-control"}))
    outros_dados=CharField(required=False,widget= Textarea(attrs={'class': "form-control"}))

    def clean_data_compra(self):
        """Faz a validação da data da compra aplicando regra de negocio: data da compra deve ser anterior a data de cadastro"""
        data_compra = self.cleaned_data.get('data_compra')
        if not(type(data_compra)==datetime.datetime):
            raise ValidationError('Data Compra invalida: não está no formato "dd/mm/aaaa"')
        data_cadastro=Equipamento.objects.get(id=self.cleaned_data['id']).data_cadastro
        if data_compra>data_cadastro:
            raise ValidationError('Data Compra invalida: a data de compra deve ser anterior a data de cadastro')
        return data_compra
    def clean_data_ultima_calibracao(self):
        """Faz a valiação da regra de negocio da data de calibração"""
        data_ultima_calibracao = self.cleaned_data.get('data_ultima_calibracao')
        if data_ultima_calibracao==None:
            return data_ultima_calibracao 
        if not(type(data_ultima_calibracao)==datetime.datetime):
            raise ValidationError('Data caliração invalida : não está no formato "dd/mm/aaaa"')
        return data_ultima_calibracao    

    def clean(self):
        """Faz a validação final dos dados e define o campo ultima alteração = agora"""
        super().clean()
        utc=pytz.timezone(TIME_ZONE) # pytz.UTC
        cd=self.cleaned_data
        cd['data_ultima_atualizacao']=utc.localize( datetime.datetime.now())
        return cd
        
class equipamentoCadastrarForm(Form):
    """formulário de cadastro de novas equipamentos"""
    nome_equipamento=CharField(widget= TextInput(attrs={'class': "form-control",'placeholder':'Nome do Equipamentos'}))
    modelo=CharField(widget= TextInput(attrs={'class': "form-control",'placeholder':'Modelo'}))
    fabricante=ModelChoiceField(queryset=Fabricante.objects.all() ,widget=Select (attrs={'class': "form-control"}))
    local=ModelChoiceField(queryset=Local_instalacao.objects.all(),widget=Select(attrs={'class': "form-control"}))
    tipo_equipamento=ModelChoiceField(queryset= Tipo_equipamento.objects.all(),widget=Select(attrs={'class': "form-control"}))
    data_compra=DateTimeField(widget=DateInput( attrs={'type': 'date', 'class': 'form-control','placeholder':'data noformato dd/mm/aaa'}))
    data_ultima_calibracao=DateTimeField(widget=DateInput( attrs={'type': 'date', 'class': 'form-control','placeholder':'data noformato dd/mm/aaa'}))
    patrimonio=CharField(widget= TextInput(attrs={'class': "form-control",'placeholder':'Numero de Patrimonio'}))
    # material_consumo=ModelMultipleChoiceField(required=False,blank=True,queryset= Material_consumo.objects.all(),widget=SelectMultiple(attrs={'class': "form-control"}))
    usuario=CharField(label="",widget=HiddenInput())
    custo_aquisição=CustomMoney(default_currency='BRL',required=True,widget= MoneyWidget(attrs={'class': "form-control",'placeholder':'0,01'}))
    responsavel=CharField(widget= TextInput(attrs={'class': "form-control",'placeholder':'Nome do responsavel pelo equipamento'}))
    potencia_eletrica=CharField(required=False,widget= TextInput(attrs={'class': "form-control",'placeholder':'Potência em W'}))
    nacionalidade=CharField(required=False,widget= TextInput(attrs={'class': "form-control",'placeholder':'Nacionalidade'}))
    tensao_eletrica=CharField(required=False,widget= TextInput(attrs={'class': "form-control",'placeholder':'tensão eletrica em V'}))
    projeto_compra=CharField(required=False,widget= TextInput(attrs={'class': "form-control",'placeholder':'Nome do Projeto'}))
    especificacao=CharField(required=False,widget= Textarea(attrs={'class': "form-control",'placeholder':'Especificação completa do equipamento, conforme nota fical ou documento de compra'}))
    outros_dados=CharField(required=False,widget= Textarea(attrs={'class': "form-control",'placeholder':'Dados adicionais'}))

    
    def clean(self):
        """Faz a valiação dos dados e das regras de negocio :
        - data de cadastro = agora
        - data de compra deve ser anterior a hoje
        - cria codigo do equipamento considerando a sigla do tipo + numero sequencial com pelo menos 3 digitos ex: AGI001"""
        super().clean()
        utc=pytz.timezone(TIME_ZONE)# pytz.UTC
        cd=self.cleaned_data
        # print(cd)
        cd['data_cadastro']=utc.localize( datetime.datetime.now())
        data_compra=cd["data_compra"]
        data_cadastro=cd["data_cadastro"]
        if data_compra>data_cadastro:
            raise ValidationError('Data Compra invalida: a data de compra deve ser anterior a data de hoje')
        tipo_equipamento=cd["tipo_equipamento"]
        tipo=Tipo_equipamento.objects.get(id=tipo_equipamento.id)
        equipamentos_tipo = Equipamento.objects.filter(codigo__icontains=tipo.sigla.upper()).order_by('-codigo')
        if len(equipamentos_tipo)==0:
            numero=1
        else:
            ultimo_equipammento=equipamentos_tipo[0]
            numero=int(ultimo_equipammento.codigo[-3:])+1
        cd['codigo']=f'{tipo.sigla.upper()}{numero:03d}'
        cd['data_ultima_atualizacao']=utc.localize( datetime.datetime.now())
        return cd
    
class cadastraTipo_equipamento(Form):
    nome=CharField(widget= TextInput(attrs={'class': "form-control",'placeholder':'Nome do tipo do equipamento'}))
    descricao=CharField(required=False,widget=Textarea(attrs={'class': "form-control",'placeholder':'Descrição breve do tipo do equipamentos e lista de equipamentos inclusos no tipo'}))
    sigla=CharField(required=False,label="",widget=HiddenInput())
   
    def clean(self):
        super().clean()
        cd=self.cleaned_data
        siglas=[]
        tipos=Tipo_equipamento.objects.all()
        for tipo in tipos:
            siglas.append(tipo.sigla)
        cd['sigla']=cd['nome'][0:3].upper()
        # print(siglas)
        i=3
        while(cd['sigla'] in siglas  and i<len(cd['nome'])):
            cd['sigla']=cd['nome'][0:2].upper()+cd['nome'][i].upper()
            i+=1
            #print(cd['sigla'])
        if i>len(cd['nome']):
            cd['sigla']=cd['nome'][0:2].upper()+'X'
            cd['sigla']=cd['sigla'].upper()
        return cd

class TipoEquipamentoForm(Form):
    id=CharField(label="",widget=HiddenInput())
    nome_tipo=CharField(widget= TextInput(attrs={'class': "form-control"}))
    descricao_tipo=CharField(widget=Textarea(attrs={'class': "form-control"}))
    sigla=CharField(required=False,label="",widget=HiddenInput())
   
    def clean(self):
        super().clean()
        cd=self.cleaned_data
        siglas=[]
        tipos=Tipo_equipamento.objects.all()
        return cd

class materialCadastraForm(ModelForm):
    id=CharField(label="",widget=HiddenInput(),required=False)
    class Meta:
        model = Material_consumo
        fields = '__all__'
        widgets = {
            'nome_material':TextInput (attrs={'class': "form-control"}),
            'fornecedor':Select (attrs={'class': "form-control"}),
            'especificacao_material':Textarea(attrs={'class': "form-control"}),
            'unidade_material':TextInput (attrs={'class': "form-control"}),
            'simbolo_unidade_material':TextInput (attrs={'class': "form-control"}),
        }

class mediaForm(ModelForm):
    #id=CharField(label="",widget=HiddenInput(),required=False)
    def clean_documentos(self):
        documentos = self.cleaned_data['documentos']
        if documentos.size > (50*1000*2**10) : # Se o Arquivo for maior que 50Mbytes
            raise ValidationError('O nome do arquivo é muito grande. Por favor, divida o arquivo ou compacte seu conteudo, o tamanho maximo aceito é 40MB.')
        if len(documentos._get_name()) > 128: # se o nome do arquivo foi maior que 128 caracteres
            raise ValidationError('O nome do arquivo é muito longo. Por favor, renomeie o arquivo reduza o tamanho para até 128 caracteres.')
        return documentos

    class Meta:
        model = Media
        fields = '__all__'
        widgets = {
            'nome':TextInput (attrs={'class': "form-control",'placeholder':'Nome de referencia do Arquivo. Ex: Manual, Nota fiscal, etc...'}),
            'equipamento':Select (attrs={'class': "form-control"}),
            'documentos':ClearableFileInput(attrs={'multiple': False,'class': "form-control"}),
            
        }
        labels = {
            'nome': 'Nome do arquivo','equipamento':'Equipamento','documentos':'Documento - Tamanho máximo do arquivo - 40MB'
        }  
class cadastrarPermissaoForm (ModelForm):
    equipamento = ModelChoiceField(queryset=Equipamento.objects.filter(ativo=True),widget=Select(attrs={'class': "form-control"}))
    usuario = ModelChoiceField(queryset=Usuario.objects.filter(ativo=True),widget=Select(attrs={'class': "form-control"}))
    class Meta:
        model = Autorizacao_equipamento
        fields = ['equipamento','usuario']
    