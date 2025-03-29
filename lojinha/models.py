from django.db import models

# Create your models here.
from django.db import models

class Escoteiro(models.Model):
    RAMOS = [
        ('lobinho', 'Lobinho'),
        ('escoteiro', 'Escoteiro'),
        ('senior', 'Sênior'),
        ('pioneiro', 'Pioneiro')
    ]

    nome = models.CharField(max_length=100)
    grupo = models.CharField(max_length=100, default='12º Grupo Escoteiro Monte Caburaí')
    ramo = models.CharField(max_length=20, choices=RAMOS)
    data_nascimento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.nome} ({self.get_ramo_display()})'


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    idade_tamanho=models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()

    def __str__(self):
        return f'Produto: {self.nome} - Idade/Tamanho {self.idade_tamanho} - Qtd Estoque: {self.estoque}'

class Venda(models.Model):
    escoteiro = models.ForeignKey(Escoteiro, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    parcelado=models.BooleanField(default=True)
    quantidade_parcelas=models.IntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Venda #{self.id} - {self.escoteiro.nome}'

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantidade * self.preco_unitario

class Parcela(models.Model):
    venda = models.ForeignKey(Venda, related_name='parcelas', on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    pago = models.BooleanField(default=False)
    data_baixa = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Parcela de R${self.valor} - Vencimento: {self.data_vencimento}'
