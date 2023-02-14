# -*- coding: utf-8 -*-
from django import forms
from django.forms import *
from .models import *
from django.forms import modelform_factory
from django.forms import BaseModelFormSet
from djmoney.forms.fields import MoneyField,MoneyWidget
import datetime
import pytz

class localFormCadastro(ModelForm):
    class Meta:
        model = Local_instalacao
        fields = '__all__'
        widgets = {
            'laboratorio': TextInput (attrs={'class': "form-control"}),
            'predio': TextInput (attrs={'class': "form-control"}),
            'piso':TextInput (attrs={'class': "form-control"}),
            'sala':TextInput (attrs={'class': "form-control"}),
            'armario':TextInput (attrs={'class': "form-control"}),
            'prateleira':TextInput (attrs={'class': "form-control"}),
            'apelido_local':TextInput (attrs={'class': "form-control"}),

        }
class localFormEditar(ModelForm):
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
            'apelido_local':TextInput (attrs={'class': "form-control"}),

        }
class  localFormlista(ModelForm):
    ListaLocais = modelformset_factory(Local_instalacao, fields=('__all__'))
    class Meta:
        model = Local_instalacao
        fields = '__all__'


class equipamentoEditarForm(Form):
    id=CharField(label="",widget=HiddenInput())
    nome_equipamento=CharField(widget= TextInput(attrs={'class': "form-control"}))
    modelo=CharField(widget= TextInput(attrs={'class': "form-control"}))
    codigo=CharField(widget= TextInput(attrs={'class': "form-control"}))
    fabricante=ModelChoiceField(queryset=Fabricante.objects.all() ,widget=Select (attrs={'class': "form-control"}))
    local=ModelChoiceField(queryset=Local_instalacao.objects.all(),widget=Select(attrs={'class': "form-control"}))
    tipo_equipamento=ModelChoiceField(queryset= Tipo_equipamento.objects.all(),widget=Select(attrs={'class': "form-control"}))
    anoAtual=datetime.datetime.now().year
    data_compra=DateTimeField(widget=SelectDateWidget(years=tuple(range(1900,anoAtual+1)),attrs={'class': "form-control"}))
    data_ultima_calibracao=DateTimeField(widget=SelectDateWidget(years=tuple(range(1900,anoAtual+1)),attrs={'class': "form-control"}))
    patrimonio=CharField(widget= TextInput(attrs={'class': "form-control"}))
    material_consumo=ModelMultipleChoiceField(required=False,blank=True,queryset= Material_consumo.objects.all(),widget=SelectMultiple(attrs={'class': "form-control"}))
    usuario=CharField(label="",widget=HiddenInput())
    custo_aquisição=MoneyField(default_currency='BRL',required=False,widget= MoneyWidget(attrs={'class': "form-control"}))
    responsavel=CharField(widget= TextInput(attrs={'class': "form-control"}))
    potencia_eletrica=CharField(required=False,widget= TextInput(attrs={'class': "form-control"}))
    nacionalidade=CharField(required=False,widget= TextInput(attrs={'class': "form-control"}))
    tensao_eletrica=CharField(required=False,widget= TextInput(attrs={'class': "form-control"}))
    projeto_compra=CharField(required=False,widget= TextInput(attrs={'class': "form-control"}))
    especificacao=CharField(required=False,widget= Textarea(attrs={'class': "form-control"}))
    outros_dados=CharField(widget= Textarea(attrs={'class': "form-control"}))

   
    def clean(self):
        super().clean()
        utc=pytz.UTC
        cd=self.cleaned_data
        cd['data_cadastro']=utc.localize( datetime.datetime.now())
        data_compra=cd["data_compra"]
        data_cadastro=cd["data_cadastro"]
        if data_compra>data_cadastro:
            raise ValidationError('Data Compra invalida: a data de compra deve ser anterior a data de hoje')
        tipo_equipamento=cd["tipo_equipamento"]
        cd['data_ultima_atualizacao']=utc.localize( datetime.datetime.now())
        return cd


class equipamentoCadastrarForm(Form):
    nome_equipamento=CharField(widget= TextInput(attrs={'class': "form-control"}))
    modelo=CharField(widget= TextInput(attrs={'class': "form-control"}))
    fabricante=ModelChoiceField(queryset=Fabricante.objects.all() ,widget=Select (attrs={'class': "form-control"}))
    local=ModelChoiceField(queryset=Local_instalacao.objects.all(),widget=Select(attrs={'class': "form-control"}))
    tipo_equipamento=ModelChoiceField(queryset= Tipo_equipamento.objects.all(),widget=Select(attrs={'class': "form-control"}))
    anoAtual=datetime.datetime.now().year
    data_compra=DateTimeField(widget=SelectDateWidget(years=tuple(range(1900,anoAtual+1)),attrs={'class': "form-control"}))
    data_ultima_calibracao=DateTimeField(widget=SelectDateWidget(years=tuple(range(1900,anoAtual+1)),attrs={'class': "form-control"}))
    patrimonio=CharField(widget= TextInput(attrs={'class': "form-control"}))
    material_consumo=ModelMultipleChoiceField(required=False,blank=True,queryset= Material_consumo.objects.all(),widget=SelectMultiple(attrs={'class': "form-control"}))
    usuario=CharField(label="",widget=HiddenInput())
    custo_aquisição=MoneyField(default_currency='BRL',required=False,widget= MoneyWidget(attrs={'class': "form-control"}))
    responsavel=CharField(widget= TextInput(attrs={'class': "form-control"}))
    potencia_eletrica=CharField(required=False,widget= TextInput(attrs={'class': "form-control"}))
    nacionalidade=CharField(required=False,widget= TextInput(attrs={'class': "form-control"}))
    tensao_eletrica=CharField(required=False,widget= TextInput(attrs={'class': "form-control"}))
    projeto_compra=CharField(required=False,widget= TextInput(attrs={'class': "form-control"}))
    especificacao=CharField(required=False,widget= Textarea(attrs={'class': "form-control"}))
    outros_dados=CharField(widget= Textarea(attrs={'class': "form-control"}))

    
    def clean(self):
        super().clean()
        utc=pytz.UTC
        cd=self.cleaned_data
        cd['data_cadastro']=utc.localize( datetime.datetime.now())
        data_compra=cd["data_compra"]
        data_cadastro=cd["data_cadastro"]
        if data_compra>data_cadastro:
            raise ValidationError('Data Compra invalida: a data de compra deve ser anterior a data de hoje')
        tipo_equipamento=cd["tipo_equipamento"]
        tipo=Tipo_equipamento.objects.get(id=tipo_equipamento.id)
        numero=len(Equipamento.objects.filter(tipo_equipamento=tipo_equipamento.id))+1
        cd['codigo']=f'{tipo.sigla.upper()}{numero:03d}'
        cd['data_ultima_atualizacao']=utc.localize( datetime.datetime.now())
        return cd

    
class cadastraTipo_equipamento(Form):
    nome=CharField(widget= TextInput(attrs={'class': "form-control"}))
    descricao=CharField(widget=Textarea(attrs={'class': "form-control"}))
    sigla=CharField(required=False,label="",widget=HiddenInput())
   
    def clean(self):
        super().clean()
        cd=self.cleaned_data
        siglas=[]
        tipos=Tipo_equipamento.objects.all()
        for tipo in tipos:
            siglas.append(tipo.sigla)
        cd['sigla']=cd['nome'][0:3].upper()
        print(siglas)
        i=3
        while(cd['sigla'] in siglas  and i<len(cd['nome'])):
            cd['sigla']=cd['nome'][0:2].upper()+cd['nome'][i].upper()
            i+=1
            print(cd['sigla'])
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


class DocumentForm(ModelForm):
    class Meta:
        model = Media
        fields = ('nome','media','equipamento')