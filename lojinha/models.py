from django.db import models
<<<<<<< HEAD
from decimal import Decimal
from datetime import date
=======
>>>>>>> 5e44138d0211cdccbf6f7bca9dcc9347531b4435

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
    idade_tamanho=models.CharField(max_length=50,null=True, blank=True)
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

<<<<<<< HEAD
# class PagamentoParcial(models.Model):
#     parcela = models.ForeignKey(Parcela, related_name='pagamentos', on_delete=models.CASCADE)
#     valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
#     data_pagamento = models.DateField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Pagamento de R${self.valor_pago} - {self.data_pagamento}"

=======
>>>>>>> 5e44138d0211cdccbf6f7bca9dcc9347531b4435
class Parcela(models.Model):
    venda = models.ForeignKey(Venda, related_name='parcelas', on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    pago = models.BooleanField(default=False)
    data_baixa = models.DateField(null=True, blank=True)

<<<<<<< HEAD
    def registrar_pagamento(self, valor):
        valor = Decimal(valor)

        if valor <= 0:
            raise ValueError("Valor do pagamento deve ser maior que zero.")

        if self.pago:
            raise ValueError("Parcela já está paga.")

        if valor > self.valor:
            raise ValueError("Valor pago excede o valor da parcela.")

        if valor == self.valor:
            # Pagamento total
            self.pago = True
            self.data_baixa = date.today()
            self.save()
        else:
            # Pagamento parcial
            # Criar nova parcela paga com o valor recebido
            Parcela.objects.create(
                venda=self.venda,
                valor=valor,
                data_vencimento=date.today(),
                pago=True,
                data_baixa=date.today()
            )

            # Atualizar esta parcela com o valor restante
            self.valor -= valor
            self.save()

    def __str__(self):
        return f'Parcela de R${self.valor} - Vencimento: {self.data_vencimento}'

=======
    def __str__(self):
        return f'Parcela de R${self.valor} - Vencimento: {self.data_vencimento}'


>>>>>>> 5e44138d0211cdccbf6f7bca9dcc9347531b4435
class Compra(models.Model):
    data = models.DateField(auto_now_add=True)
    fornecedor = models.CharField(max_length=200)
    total_gasto = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Compra #{self.id} - Fornecedor: {self.fornecedor} - Total: R${self.total_gasto}'

    def calcular_total(self):
        self.total_gasto = sum(item.subtotal() for item in self.itens.all())
        self.save()

class ItemCompra(models.Model):
    compra = models.ForeignKey(Compra, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.produto.estoque += self.quantidade  # Atualiza o estoque
        self.produto.save()
        self.compra.calcular_total()  # Atualiza o total gasto na compra
