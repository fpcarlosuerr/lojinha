# lojinha/urls.py
from django.urls import path
from .views import nova_venda, cadastrar_produto, editar_produto, excluir_produto, inicio

urlpatterns = [
    path('',inicio,name='inicio'),
    path('nova_venda', nova_venda, name='nova_venda'),
    path('produtos/', cadastrar_produto, name='cadastrar_produto'),
    path('produtos/<int:pk>/editar/', editar_produto, name='editar_produto'),
    path('produtos/<int:pk>/excluir/', excluir_produto, name='excluir_produto'),
]

