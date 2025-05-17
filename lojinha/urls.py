# lojinha/urls.py
from django.urls import path
#from .views import nova_venda, cadastrar_produto, editar_produto, excluir_produto, inicio, listar_compras, nova_compra, get_preco_produto, listar_vendas_abertas, marcar_parcela_pago, detalhar_venda
from . import views

urlpatterns = [
    path('',views.inicio,name='inicio'),
    path('nova_venda', views.nova_venda, name='nova_venda'),
    path('produtos/', views.cadastrar_produto, name='cadastrar_produto'),
    path('produtos/<int:pk>/editar/', views.editar_produto, name='editar_produto'),
    path('produtos/<int:pk>/excluir/', views.excluir_produto, name='excluir_produto'),
    path('compras/', views.listar_compras, name='listar_compras'),
    path('compras/nova/', views.nova_compra, name='nova_compra'),
    path('compras/detalhes/<int:compra_id>/', views.detalhar_compra, name='detalhar_compra'),
    path('get_preco_produto/<int:produto_id>/', views.get_preco_produto, name='get_preco_produto'),
    path('vendas/abertas/', views.listar_vendas_abertas, name='listar_vendas_abertas'),
    path('venda/detalhe/<int:venda_id>/', views.detalhar_venda, name='detalhar_venda'),
    path('parcela/<int:parcela_id>/pagar/', views.marcar_parcela_pago, name='marcar_parcela_pago'),
    path('escoteiro/lista', views.listar_escoteiros, name='listar_escoteiros'),
    path('escoteiro/novo/', views.cadastrar_escoteiro, name='novo_escoteiro'),
    path('escoteiro/editar/<int:pk>/', views.cadastrar_escoteiro, name='editar_escoteiro'),
    path('escoteiro/excluir/<int:pk>/', views.excluir_escoteiro, name='excluir_escoteiro'),
    path('relatorio_vendas/', views.relatorio_vendas, name='relatorio_vendas'),
<<<<<<< HEAD
    path('parcelas/<int:parcela_id>/pagar/', views.pagar_parcela, name='pagar_parcela'),
=======
>>>>>>> 5e44138d0211cdccbf6f7bca9dcc9347531b4435
]

