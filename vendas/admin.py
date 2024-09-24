from django.contrib import admin

from vendas.models import Venda


# Register your models here.
@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    """
    Configura a interface de administração do Django para o modelo
    Venda.

    Attributes:
        list_display (tuple): Campos a serem exibidos na
        listagem do modelo.

        search_fields (tuple): Campos pelos quais a pesquisa pode
        ser feita.

        list_filter (tuple): Campos pelos quais a lista pode ser
        filtrada.
    """

    list_display = (
        'cliente',
        'vendedor',
        'produto',
        'quantidade',
        'valor_unitario',
        'valor_total',
        'data_da_venda',
    )

    search_fields = ('cliente', 'vendedor', 'produto', 'data_da_venda')
