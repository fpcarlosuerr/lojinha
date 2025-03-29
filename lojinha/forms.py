# lojinha/forms.py

from django import forms
from .models import Escoteiro, Produto, Venda, ItemVenda, Parcela

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
    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade']

    def clean(self):
        cleaned_data = super().clean()
        produto = cleaned_data.get('produto')
        quantidade = cleaned_data.get('quantidade')

        if produto and quantidade:
            if quantidade > produto.estoque:
                raise forms.ValidationError(
                    f"A quantidade solicitada ({quantidade}) excede o estoque disponível ({produto.estoque})."
                )
                
class ParcelaForm(forms.ModelForm):
    class Meta:
        model = Parcela
        fields = ['valor', 'data_vencimento', 'pago']
