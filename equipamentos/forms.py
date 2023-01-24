from django import forms
from django.forms import *
from .models import *

class localForm(ModelForm):
    
    
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
        