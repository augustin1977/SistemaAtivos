from django import forms
from django.forms import *
from equipamentos.models import *
from django.forms import modelform_factory
from django.forms import BaseModelFormSet

from cadastro_equipamentos.settings import TIME_ZONE
import datetime
import pytz

class localFormCadastro(ModelForm):
    class Meta:
        model = Equipamento
        fields = 'nome_equipamento'
        widgets = {
            'nome_equipamento': Select (attrs={'class': "form-control"}),
        }
