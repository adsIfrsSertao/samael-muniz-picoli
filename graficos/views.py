from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from vendas.models import Venda
from .forms import FiltroGraficoForm

def gerar_grafico(request):
    form = FiltroGraficoForm(request.GET or None)

    if form.is_valid():
        vendedor = form.cleaned_data.get('vendedor')
        cliente = form.cleaned_data.get('cliente')
        ano = form.cleaned_data.get('ano')
        tipo_grafico = form.cleaned_data.get('tipo_grafico')

        # Filtrando as vendas
        vendas = Venda.objects.all()

        if vendedor:
            print('selecionou vendedor')
            vendas = vendas.filter(vendedor=vendedor)

        if cliente:
            print('selecionou cliente')
            vendas = vendas.filter(cliente=cliente)

        if ano:
            print('selecionou ano')
            vendas = vendas.filter(data_da_venda__year=ano)
        
        # Agrupando os resultados para Vendedor
        if vendedor and not cliente and not ano:
            resultados = (
                vendas
                .values('data_da_venda__year')  # Agrupa por ano
                .annotate(total=Sum('valor_total') if tipo_grafico == 'valor' else Sum('quantidade'))  # Soma com base na seleção
                .order_by('data_da_venda__year')  # Ordena por ano
            )
        
        # Agrupando os resultados para Vendedor e Cliente
        elif vendedor and cliente and not ano:
            resultados = (
                vendas
                .values('data_da_venda__year', 'produto__produto')  # Agrupa por ano e produto
                .annotate(
                    total=Sum('quantidade') if tipo_grafico == 'quantidade' else Sum('valor_total')
                )
                .order_by('data_da_venda__year', 'produto__produto')  # Ordena por ano e produto
            )

        # Agrupando os resultados para Vendedor e Ano
        elif vendedor and ano:
            resultados = (
                vendas
                .values('cliente__nome')  # Agrupa por cliente
                .annotate(
                    total=Sum('quantidade') if tipo_grafico == 'quantidade' else Sum('valor_total')
                )
                .order_by('cliente__nome')  # Ordena por nome do cliente
            )
        try:
            # Convertendo os resultados em uma lista de dicionários
            dados_grafico = list(resultados)
            print(dados_grafico)  # Adicione esta linha para depuração
            return JsonResponse(dados_grafico, safe=False)
        except UnboundLocalError:
            ...

    return render(request, 'grafico_vendas.html', {'form': form})
