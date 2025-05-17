# lojinha/forms.py

from django import forms
from .models import Escoteiro, Produto, Venda, ItemVenda, Parcela, Compra, ItemCompra


class EscoteiroForm(forms.ModelForm):
    class Meta:
        model = Escoteiro
        fields = ['nome', 'grupo', 'ramo', 'data_nascimento']

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome','idade_tamanho', 'preco', 'estoque']

class VendaForm(forms.ModelForm):
    parcelado = forms.BooleanField(required=False, initial=True, label="Parcelar?")
    quantidade_parcelas = forms.IntegerField(min_value=1, initial=1, label="Número de parcelas")

    class Meta:
        model = Venda
        fields = ['escoteiro', 'parcelado', 'quantidade_parcelas']

class ItemVendaForm(forms.ModelForm):
    preco_unitario = forms.DecimalField(max_digits=10, decimal_places=2, required=True, label="Preço Unitário")

    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade', 'preco_unitario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adiciona um atributo data-preco ao campo de produto para manipulação via JavaScript
        self.fields['produto'].widget.attrs.update({'class': 'produto-selecionado'})

        # Se o produto já estiver definido, preenche o preço unitário
        #if self.instance and self.instance.produto:
        if self.instance and getattr(self.instance, 'produto_id', None):    
            self.fields['preco_unitario'].initial = self.instance.produto.preco

    def clean(self):
        cleaned_data = super().clean()
        produto = cleaned_data.get('produto')
        preco_unitario = cleaned_data.get('preco_unitario')
        quantidade = cleaned_data.get('quantidade')
        
        # Se o preço unitário não foi alterado, usamos o preço do produto
        if not preco_unitario:
            preco_unitario = produto.preco  # Usando o preço do produto como fallback

        if produto and quantidade:
            if quantidade > produto.estoque:
                raise forms.ValidationError(
                    f"A quantidade solicitada ({quantidade}) excede o estoque disponível ({produto.estoque})."
                )
        cleaned_data['preco_unitario'] = preco_unitario
        return cleaned_data
                
class ParcelaForm(forms.ModelForm):
    class Meta:
        model = Parcela
        fields = ['valor', 'data_vencimento', 'pago']

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['fornecedor']

class ItemCompraForm(forms.ModelForm):
    class Meta:
        model = ItemCompra
        fields = ['produto', 'quantidade', 'preco_unitario']

class FiltroVendasForm(forms.Form):
    data_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Data Início')
    data_fim = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Data Fim')

class PagamentoParcialForm(forms.Form):
    parcela_id = forms.IntegerField(widget=forms.HiddenInput())
    valor_pago = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    data_fim = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Data Fim')
