from datetime import datetime

from django import forms

from clientes.models import Cliente
from vendedores.models import Vendedor

class FiltroGraficoForm(forms.Form):
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


