from django import forms
from django.forms import *
from .models import *
from django.forms import modelform_factory
from django.forms import BaseModelFormSet
from usuarios.models import *


class EditaUsuarioForm (ModelForm):
    id=CharField(label="",widget=HiddenInput())
    class Meta:
        model = Usuario
        fields = ['id','nome','chapa','email','tipo','primeiro_acesso']
        widgets = {
            'nome':TextInput(attrs={'class': "form-control"}),
            'chapa':NumberInput (attrs={'class': "form-control"}),
            'email':EmailInput(attrs={'class': "form-control"}),
            'tipo': Select (attrs={'class': "form-control"}),
            'primeiro_acesso': CheckboxInput (attrs={'class': "form-control"}),
            }
        
