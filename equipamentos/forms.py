from django import forms
from .models import *

class localForm(forms.ModelForm):
    class Meta:
        model = Local_instalacao
        fields = ['predio','piso','sala','armario','prateleira']