from django import forms
from django.forms import *
from .models import *
from django.forms import modelform_factory

class localFormCadastro(ModelForm):
    class Meta:
        model = Local_instalacao
        fields = '__all__'
        widgets = {
            'predio': TextInput (attrs={'class': "form-control"}),
            'piso':TextInput (attrs={'class': "form-control"}),
            'sala':TextInput (attrs={'class': "form-control"}),
            'armario':TextInput (attrs={'class': "form-control"}),
            'prateleira':TextInput (attrs={'class': "form-control"}),
            'apelido_local':TextInput (attrs={'class': "form-control"}),

        }
        def clean(self):
            super().clean()
class  localFormlista(ModelForm):
     ListaLocais = modelformset_factory(Local_instalacao, fields=('__all__'))
     class Meta:
        model = Local_instalacao
        fields = '__all__' 