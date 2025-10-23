from django.db import models
from usuarios.models import *
from equipamentos.models import Local_instalacao


class Cor(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    tonalidade = models.CharField(max_length=9, unique=True)  # "#RRGGBB" ou "#RRGGBBOO"
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - {'Ativa' if self.ativa else 'Inativa'}"

    @property
    def css_color(self) -> str:
        """
        Retorna uma string CSS válida ignorando o canal alfa quando existir.
        Aceita:
          - "#RRGGBBOO" -> "#RRGGBB"
          - "#RRGGBB"   -> "#RRGGBB"
          - "RRGGBBOO"  -> "#RRGGBB"
          - "RRGGBB"    -> "#RRGGBB"
          - "#RGB" / "RGB" -> expande para "#RRGGBB"
        Qualquer coisa fora disso, cai num fallback "#000000".
        """
        t = (self.tonalidade or "").strip().upper()

        # remove prefixos e garante '#'
        if t.startswith("#"):
            hex_ = t[1:]
        else:
            hex_ = t

        # só aceita 3, 6 ou 8 dígitos hex
        if len(hex_) == 8:       # RRGGBBOO -> corta OO
            hex_ = hex_[:6]
        elif len(hex_) == 3:     # RGB -> expande
            hex_ = "".join(c * 2 for c in hex_)
        elif len(hex_) == 6:
            pass
        else:
            return "#000000"     # fallback

        # valida caracteres
        try:
            int(hex_, 16)
        except ValueError:
            return "#000000"

        return f"#{hex_}"
    
class Projeto(models.Model):
    nome=models.CharField(max_length=255,unique=True)
    cliente=models.CharField(max_length=255)
    data_criacao=models.DateTimeField(auto_now_add=True)
    ativo=models.BooleanField(default=True)
    cor=models.ForeignKey(Cor, on_delete=models.PROTECT, null=False, blank=False)
    responsavel=models.ForeignKey(Usuario, on_delete=models.PROTECT, null=False, blank=False)
    def __str__(self):
        return f"{self.nome} - {self.cliente} - {self.cor.nome} - {self.responsavel.nome}"
class Amostra(models.Model):
    nome=models.CharField(max_length=255)
    projeto=models.ForeignKey(Projeto, on_delete=models.CASCADE, null=False, blank=False)
    data_cadastro=models.DateTimeField(auto_now_add=True)
    data_alteracao=models.DateTimeField(auto_now=True)
    data_recebimento=models.DateField(null=False, blank=False)
    data_fim=models.DateField(null=True, blank=True)
    prazo_dias=models.IntegerField()
    def __str__(self):
        return f"{self.nome} - {self.projeto.nome}"
class Etiqueta(models.Model):
    amostra=models.ForeignKey(Amostra, on_delete=models.CASCADE, null=False, blank=False)
    data_criacao=models.DateTimeField(auto_now_add=True)
    data_alteracao=models.DateTimeField(auto_now=True)
    local_instalacao=models.ForeignKey(Local_instalacao, on_delete=models.PROTECT, null=True, blank=True)
    massa=models.DecimalField(max_digits=10, decimal_places=3,null=False, blank=False)
    codigo_humano=models.CharField(max_length=255,unique=True)
    codigo_numerico=models.CharField(max_length=255, unique=True)
    observacao=models.TextField(blank=True)
    def __str__(self):
        cor_nome = self.amostra.projeto.cor.nome
        return f"{self.codigo_humano} - {self.amostra.nome} - {self.codigo_numerico} - {cor_nome}"

class SequenciaEtiqueta(models.Model):
    proximo_numero = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Sequência atual: {self.proximo_numero}"

    class Meta:
        verbose_name = "Controle de sequência de etiquetas"
        verbose_name_plural = "Controle de sequência de etiquetas"
