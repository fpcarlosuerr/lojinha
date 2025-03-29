# lojinha/urls.py
from django.urls import path
from .views import nova_venda

urlpatterns = [
    path('nova-venda/', nova_venda, name='nova_venda'),
    path('', nova_venda, name='nova_venda'),
]

