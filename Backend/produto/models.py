from django.db import models
from django.contrib.auth.models import User


class Categoria(models.TextChoices):
    # ENUMARATOR = 'VALOR', 'RÓTULO'
    ELETRONICOS = 'ELE', 'Eletrônicos'
    ROUPAS = 'ROU', 'Roupas'
    LIVROS = 'LIV', 'Livros'
    MOVEIS = 'MOV', 'Móveis'
    OUTROS = 'OUT', 'Outros'


class Produto(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, help_text="Nome do produto")
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Vendedor do produto")
    categoria = models.CharField(max_length=100, choices=Categoria.choices,default=Categoria.OUTROS, help_text="Categoria do produto")
    preco = models.DecimalField(max_digits=16, decimal_places=2, help_text="Preço do produto")
    foto = models.ImageField(upload_to='fotos_produtos/', null=True, blank=True, help_text="Foto do produto")
    descricao = models.TextField(help_text="Descrição do produto")

    def __str__(self):
        return f"{self.nome} - {self.vendedor.username}"
