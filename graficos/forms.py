from datetime import datetime

from django import forms

from clientes.models import Cliente
from vendedores.models import Vendedor

class FiltroGraficoForm(forms.Form):
    """
    Formulário para filtrar os dados do gráfico de vendas.

    Esta classe de formulário permite que o usuário selecione critérios para
    filtrar as vendas, incluindo vendedor, cliente, ano e tipo de gráfico.

    Attributes:
        vendedor: Campo para selecionar um vendedor da lista de vendedores disponíveis.
        cliente: Campo para selecionar um cliente da lista de clientes disponíveis.
        ano: Campo para selecionar um ano, com opções de 2020 até o ano atual.
        tipo_grafico: Campo para selecionar o tipo de gráfico a ser exibido,
        que pode ser baseado na quantidade total ou no valor monetário das vendas.
    """

    vendedor = forms.ModelChoiceField(
        queryset=Vendedor.objects.all(), 
        required=False, 
        label="Vendedor"
    )
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(), 
        required=False, 
        label="Cliente"
    )
    ano = forms.ChoiceField(
        choices=[('', 'Selecione um ano')] + [(str(ano), str(ano)) for ano in range(2020, datetime.now().year + 1)],
        required=False,
        label="Ano"
    )
    tipo_grafico = forms.ChoiceField(
        choices=[
            ('quantidade', 'Quantidade Total'),
            ('valor', 'Valor Monetário'),
        ],
        required=True,
        label="Tipo de Gráfico"
    )


