from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render

from vendas.models import Venda

from .forms import FiltroGraficoForm


def gerar_grafico(request):
    """
    Gera um gráfico de vendas com base nos filtros fornecidos pelo usuário.

    Este método processa os filtros de vendedor, cliente, ano e tipo de
    gráfico enviados via request. Dependendo dos filtros aplicados, ele
    consulta o banco de dados para agrupar e somar as vendas, retornando
    os resultados em formato JSON para visualização em um gráfico.

    Args:
        request: objeto HttpRequest que contém dados da solicitação,
        incluindo os parâmetros do formulário de filtro.

    Returns:
        JsonResponse: um objeto JSON contendo os dados agrupados para
        o gráfico se os filtros forem válidos.
        Renderização do template 'grafico_vendas.html' se os filtros
        não forem válidos ou não forem fornecidos.
    """
    form = FiltroGraficoForm(request.GET or None)

    if form.is_valid():
        vendedor = form.cleaned_data.get('vendedor')
        cliente = form.cleaned_data.get('cliente')
        ano = form.cleaned_data.get('ano')
        tipo_grafico = form.cleaned_data.get('tipo_grafico')
        quantidade_opcoes = form.cleaned_data.get('quantidade_opcoes')

        # Filtrando as vendas
        vendas = Venda.objects.all()

        if vendedor:
            vendas = vendas.filter(vendedor=vendedor)

        if cliente:
            vendas = vendas.filter(cliente=cliente)

        if ano:
            vendas = vendas.filter(data_da_venda__year=ano)

        # Agrupando os resultados
        if vendedor and not cliente and not ano:
            resultados = (
                vendas.values('data_da_venda__year')
                .annotate(
                    total=Sum('valor_total')
                    if tipo_grafico == 'valor'
                    else Sum('quantidade')
                )
                .order_by('data_da_venda__year')
            )

        elif vendedor and cliente and not ano:
            resultados = (
                vendas.values('data_da_venda__year', 'produto__produto')
                .annotate(
                    total=Sum('quantidade')
                    if tipo_grafico == 'quantidade'
                    else Sum('valor_total')
                )
                .order_by('-total')
            )

        elif vendedor and ano and not cliente:
            resultados = (
                vendas.values('cliente__nome')
                .annotate(
                    total=Sum('quantidade')
                    if tipo_grafico == 'quantidade'
                    else Sum('valor_total')
                )
                .order_by('-total')
            )

        elif cliente and not vendedor and not ano:
            resultados = (
                vendas.values('data_da_venda__year')
                .annotate(
                    total=Sum('valor_total')
                    if tipo_grafico == 'valor'
                    else Sum('quantidade')
                )
                .order_by('data_da_venda__year')
            )

        elif cliente and ano and not vendedor:
            resultados = (
                vendas.values('produto__produto')
                .annotate(
                    total=Sum('quantidade')
                    if tipo_grafico == 'quantidade'
                    else Sum('valor_total')
                )
                .order_by('-total')
            )

        elif ano and not cliente and not vendedor:
            resultados = (
                vendas.values('cliente__nome')
                .annotate(
                    total=Sum('quantidade')
                    if tipo_grafico == 'quantidade'
                    else Sum('valor_total')
                )
                .order_by('-total')
            )

        elif ano and cliente and vendedor:
            resultados = (
                vendas.values('produto__produto')
                .annotate(
                    total=Sum('quantidade')
                    if tipo_grafico == 'quantidade'
                    else Sum('valor_total')
                )
                .order_by('-total')
            )

        if quantidade_opcoes and quantidade_opcoes != 'all':
            n = int(quantidade_opcoes)

            if n > 0:
                resultados = resultados[:n]
            else:
                n = abs(n)
                resultados = resultados.order_by('total')[:n]

        try:
            dados_grafico = list(resultados)
            print(dados_grafico)
            return JsonResponse(dados_grafico, safe=False)
        except UnboundLocalError:
            pass

    return render(request, 'grafico_vendas.html', {'form': form})
