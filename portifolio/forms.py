from django.forms import Form, CharField, BooleanField, TextInput, HiddenInput
from .models import Cor

class CorForm(Form):
    id = CharField(label="", required=False, widget=HiddenInput())
    nome = CharField(widget=TextInput(attrs={'class': "form-control"}))
    tonalidade = CharField(widget=TextInput(attrs={'class': "form-control", 'placeholder': "#RRGGBB"}))
    ativa = BooleanField(required=False, label="Ativa")

    def clean(self):
        super().clean()
        cd = self.cleaned_data

        nome = cd.get("nome")
        tonalidade = cd.get("tonalidade")
        id_val = cd.get("id") or None  # evita string vazia

        # validação de nome duplicado
        qs = Cor.objects.filter(nome__iexact=nome)
        if id_val:
            qs = qs.exclude(id=id_val)
        if nome and qs.exists():
            self.add_error("nome", "Já existe uma cor com esse nome.")

        # validação de tonalidade duplicada
        qs = Cor.objects.filter(tonalidade__iexact=tonalidade)
        if id_val:
            qs = qs.exclude(id=id_val)
        if tonalidade and qs.exists():
            self.add_error("tonalidade", "Essa tonalidade já está cadastrada.")

        return cd
