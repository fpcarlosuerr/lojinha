# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.utils.timezone import now
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from datetime import timedelta, date
from .models import Venda, ItemVenda, Parcela, Produto, Compra, ItemCompra, Escoteiro
from .forms import VendaForm, ItemVendaForm, ProdutoForm, CompraForm, ItemCompraForm, EscoteiroForm, FiltroVendasForm
from django.contrib import messages

def listar_compras(request):
    compras = Compra.objects.all()
    return render(request, 'lojinha/listar_compras.html', {'compras': compras})

def nova_compra(request):
    ItemCompraFormSet = modelformset_factory(ItemCompra, form=ItemCompraForm, extra=1, can_delete=True)

    if request.method == 'POST':
        compra_form = CompraForm(request.POST)
        item_formset = ItemCompraFormSet(request.POST)

        if compra_form.is_valid() and item_formset.is_valid():
            compra = compra_form.save()
            itens = item_formset.save(commit=False)
            
            for item in itens:
                item.compra = compra
                item.save()

            compra.calcular_total()
            return redirect('listar_compras')

    else:
        compra_form = CompraForm()
        item_formset = ItemCompraFormSet(queryset=ItemCompra.objects.none())

    return render(request, 'lojinha/nova_compra.html', {'compra_form': compra_form, 'item_formset': item_formset})


def inicio(request):
    return render(request, 'lojinha/home.html')

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
                    item.preco_unitario = form.cleaned_data['preco_unitario']
                    #item.preco_unitario = item.produto.preco
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

            return redirect('ad min:index')  # ou alguma página de confirmação

    else:
        venda_form = VendaForm()
        formset = ItemVendaFormSet(queryset=ItemVenda.objects.none())

    return render(request, 'lojinha/nova_venda.html', {
        'venda_form': venda_form,
        'formset': formset,
    })


# Listar produtos
def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'lojinha/produto_form.html', {'produtos': produtos})

# Cadastrar produto

def cadastrar_produto(request):
    produtos = Produto.objects.all()
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('cadastrar_produto')
    else:
        form = ProdutoForm()
    return render(request, 'lojinha/produto_form.html', 
                  {
                      'form': form, 
                      'titulo': 'Cadastrar Produto', 
                      'produtos': produtos
                  })

# Editar produto

def editar_produto(request, pk):
    produtos = Produto.objects.all()
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('cadastrar_produto')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'lojinha/produto_form.html', {'form': form, 'titulo': 'Editar Produto','produtos': produtos})

# Excluir produto

def excluir_produto(request, pk):
    produtos = Produto.objects.all()
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'GET':
        produto.delete()
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('cadastrar_produto')
    return render(request, 'lojinha/produto_form.html', {'produto': produto,'produtos': produtos})

#def get_preco_produto(request, produto_id):
#    produto = Produto.objects.get(id=produto_id)
#    return JsonResponse({'preco': float(produto.preco)})

def get_preco_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    return JsonResponse({'preco': float(produto.preco)})

def listar_vendas_abertas(request):
    # Busca todas as parcelas não pagas
    parcelas_em_aberto = Parcela.objects.filter(pago=False)
    # Busca as vendas associadas às parcelas em aberto
    vendas_em_aberto = Venda.objects.filter(parcelas__in=parcelas_em_aberto).distinct()
    # Passa as vendas em aberto para o template
    return render(request, 'lojinha/listar_vendas_abertas.html', {'vendas': vendas_em_aberto})

def detalhar_venda(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)
    parcelas = venda.parcelas.all()
    
    return render(request, 'lojinha/detalhar_venda.html', {'venda': venda, 'parcelas': parcelas})

def marcar_parcela_pago(request, parcela_id):
    parcela = get_object_or_404(Parcela, id=parcela_id)
    parcela.pago = True
    parcela.data_baixa = now().date()  # Marca a data de baixa
    parcela.save()
    return redirect('detalhar_venda', venda_id=parcela.venda.id)

def cadastrar_escoteiro(request, pk=None):
    if pk:
        escoteiro = get_object_or_404(Escoteiro, pk=pk)
    else:
        escoteiro = None

    if request.method == 'POST':
        form = EscoteiroForm(request.POST, instance=escoteiro)
        if form.is_valid():
            form.save()
            return redirect('listar_escoteiros')
    else:
        form = EscoteiroForm(instance=escoteiro)

    return render(request, 'lojinha/cadastrar_escoteiro.html', {'form': form})

def listar_escoteiros(request):
    escoteiros = Escoteiro.objects.all()
    return render(request, 'lojinha/listar_escoteiros.html', {'escoteiros': escoteiros})

def excluir_escoteiro(request, pk):
    escoteiro = get_object_or_404(Escoteiro, pk=pk)
    escoteiro.delete()
    messages.success(request, "Escoteiro excluído com sucesso!")
    return redirect('listar_escoteiros')

def relatorio_vendas(request):
    vendas = None
    form = FiltroVendasForm(request.GET or None)
    
    current_date = date.today()

    if request.method == 'GET' and form.is_valid():
        
        data_inicio = form.cleaned_data['data_inicio']
        data_fim = form.cleaned_data['data_fim']

        # Filtro de vendas por período
        vendas = Venda.objects.filter(data__range=[data_inicio, data_fim])
        
        # Verifica se as parcelas estão em aberto, vencendo ou em atraso
        # Verifica se as parcelas estão em aberto, vencendo ou em atraso
        for venda in vendas:
            parcelas = Parcela.objects.filter(venda=venda)
            venda.parcelas_status = []

            total_pago = 0
            total_em_aberto = 0
            for parcela in parcelas:
                if parcela.pago:
                    total_pago += parcela.valor
                else:
                    total_em_aberto += parcela.valor

                # Adiciona o status da parcela
                if parcela.data_vencimento > current_date:
                    # A parcela ainda vai vencer
                    status = f'A vencer - R$ {parcela.valor} em aberto'
                elif parcela.data_vencimento < current_date and not parcela.pago:
                    # A parcela está em atraso
                    status = f'Em atraso - R$ {parcela.valor} em aberto'
                else:
                    # A parcela está paga
                    status = f'Pago - R$ {parcela.valor} pago'

                venda.parcelas_status.append(status)

            # Calcula o total pago e em aberto da venda
            venda.total_pago = total_pago
            venda.total_em_aberto = total_em_aberto
        

    return render(request, 'lojinha/relatorio_vendas.html', {
        'form': form,
        'vendas': vendas,
        'current_date': current_date
    })