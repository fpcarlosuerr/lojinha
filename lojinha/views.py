# views.py
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.utils.timezone import now
from datetime import timedelta
from .models import Venda, ItemVenda, Parcela
from .forms import VendaForm, ItemVendaForm
from django.contrib import messages

def nova_venda(request):
    #ItemVendaFormSet = modelformset_factory(ItemVenda, form=ItemVendaForm, extra=3)
    ItemVendaFormSet = modelformset_factory(ItemVenda, form=ItemVendaForm, extra=1, can_delete=True)


    if request.method == 'POST':
        venda_form = VendaForm(request.POST)
        formset = ItemVendaFormSet(request.POST, queryset=ItemVenda.objects.none())

        if venda_form.is_valid() and formset.is_valid():
            venda = venda_form.save(commit=False)
            venda.total = 0
            venda.save()

            total = 0
            for form in formset:
                if not form.is_valid():
                    for error in form.non_field_errors():
                        messages.error(request, error)
                if form.cleaned_data:
                    item = form.save(commit=False)
                    item.venda = venda
                    item.preco_unitario = item.produto.preco
                    item.save()
                    total += item.subtotal()

                    # Atualiza o estoque do produto
                    produto = item.produto
                    produto.estoque -= item.quantidade
                    produto.save()

            venda.total = total
            venda.save()

            if venda.parcelado:
                valor_parcela = round(total / venda.quantidade_parcelas, 2)
                for i in range(venda.quantidade_parcelas):
                    data_venc = now().date() + timedelta(days=30 * i)
                    Parcela.objects.create(venda=venda, valor=valor_parcela, data_vencimento=data_venc)

            return redirect('admin:index')  # ou alguma página de confirmação

    else:
        venda_form = VendaForm()
        formset = ItemVendaFormSet(queryset=ItemVenda.objects.none())

    return render(request, 'lojinha/venda_form.html', {
        'venda_form': venda_form,
        'formset': formset,
    })
