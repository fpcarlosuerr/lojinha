from django.contrib import admin
from .models import Escoteiro, Produto, Venda, ItemVenda, Parcela

# Inlines
class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1

class ParcelaInline(admin.TabularInline):
    model = Parcela
    extra = 1

# Admins personalizados
class EscoteiroAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'ramo', 'grupo']

class ProdutoAdmin(admin.ModelAdmin):
    search_fields = ['nome']

class VendaAdmin(admin.ModelAdmin):
    inlines = [ItemVendaInline, ParcelaInline]
    search_fields = ['escoteiro__nome']

# Registro no admin
admin.site.register(Escoteiro, EscoteiroAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Venda, VendaAdmin)
