import io

import pandas as pd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from clientes.models import Cliente
from contrib.limpar_arquivo import tratar_dados
from produtos.models import Produto
from vendedores.models import Vendedor

from .forms import UploadFileForm, VendaForm
from .models import Venda


# Create your views here.
class VendaList(LoginRequiredMixin, ListView):
    """
    Classe-based view para listar Vendas.

    Atributos:
        model (Model): O modelo que será utilizado na listagem.
        template_name (str): O nome do template que será renderizado.
        paginate_by (int): Quantidade de itens por página na paginação.
    """

    model = Venda
    template_name = 'lista_vendas.html'
    paginate_by = 15
    context_object_name = 'vendas'

    def get_queryset(self):
        """
        Retorna o conjunto de consultas para a listagem de vendas.

        O método filtra as vendas com base nos parâmetros de busca 'cliente'
        e 'vendedor' fornecidos na requisição GET. Se qualquer um dos
        parâmetros estiver presente e não for vazio, o queryset será filtrado
        para incluir apenas as vendas correspondentes.

        Returns:
            QuerySet: O conjunto de vendas filtrado.
        """
        queryset = super().get_queryset()
        cliente = self.request.GET.get('cliente', '')
        vendedor = self.request.GET.get('vendedor', '')
        if cliente:
            queryset = queryset.filter(cliente__nome__istartswith=cliente)
        if vendedor:
            queryset = queryset.filter(vendedor__nome__istartswith=vendedor)

        return queryset


class CriarVenda(LoginRequiredMixin, CreateView):
    """
    View baseada em classe para criar um novo Venda.

    Atributos:
        model (Model): O modelo que será utilizado na view.
        template_name (str): O nome do template que será renderizado.
        form_class (Form): O formulário que será utilizado
        para criar o objeto.
    """

    model = Venda
    template_name = 'formulario_venda.html'
    form_class = VendaForm
    success_url = reverse_lazy('vendas:lista_vendas')

    def form_valid(self, form):
        messages.success(self.request, 'Venda inserido com sucesso!')
        return super().form_valid(form)


class EditarVenda(LoginRequiredMixin, UpdateView):
    """
    View baseada em classe para editar um Venda.

    Atributos:
        model (Model): O modelo que será utilizado na view.
        template_name (str): O nome do template que será renderizado.
        form_class (Form): O formulário que será utilizado
        para criar o objeto.
    """

    model = Venda
    template_name = 'formulario_venda.html'
    form_class = VendaForm
    success_url = reverse_lazy('vendas:lista_vendas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venda = self.object
        context['venda'].valor_unitario = '{:.2f}'.format(
            venda.valor_unitario
        ).replace(',', '.')
        context['venda'].valor_total = '{:.2f}'.format(
            venda.valor_total
        ).replace(',', '.')
        return context

    def form_valid(self, form):
        print(
            form.cleaned_data
        )  # Depuração: verifique o conteúdo dos dados do formulário
        messages.success(self.request, 'Venda atualizado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)  # Verifica os erros do formulário
        return super().form_invalid(form)


class DeletarVenda(LoginRequiredMixin, DeleteView):
    """
    View baseada em classe para deletar uma venda.

    Attributes:
        model (Model): O modelo que será utilizado na view.
        success_url (Django.Url): Página que será direcionada após a conclusão.
    """

    model = Venda
    success_url = reverse_lazy('vendas:lista_vendas')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Venda removido com sucesso!')
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required(login_url='usuarios/login/')
def detalhe_venda(request, pk):
    """
    View para exibir os detalhes de uma venda específica.

    Args:
        request (HttpRequest): O objeto de solicitação HTTP.
        pk (int): A chave primária da venda a ser exibido.

    Returns:
        HttpResponse: A resposta HTTP com o template
        `detalhe_venda.html` renderizado.
    """
    nome_template = 'detalhe_venda.html'
    venda = get_object_or_404(Venda, pk=pk)
    contexto = {'venda': venda}
    return render(request, template_name=nome_template, context=contexto)


@login_required(login_url='/usuarios/login/')
def venda_json(request, pk):
    """
    Retorna os dados de um Venda específico em formato JSON.

    Este método filtra o Venda com base na chave primária
    fornecida (pk), converte os dados principais do Venda
    em um formato de dicionário utilizando o método `dict_to_json`
    e retorna os dados como uma resposta JSON.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        pk (int): A chave primária do Venda a ser recuperado.

    Returns:
        JsonResponse: Um objeto de resposta JSON contendo os
        dados do Venda.
    """
    venda = get_object_or_404(Venda, pk=pk)
    data = venda.dict_to_json()
    return JsonResponse({'data': data})


@login_required(login_url='/usuarios/login/')
def upload_vendas(request):
    """
    Processa o upload de um arquivo contendo informações de vendas.

    Esta view permite que usuários autenticados façam o upload de um arquivo
    (ex: Excel ou CSV) com dados de vendas. Após o upload, os dados são
    tratados e inseridos no banco de dados. A função verifica se os clientes,
    vendedores e produtos associados às vendas já existem, criando-os se
    necessário. Vendas duplicadas (baseadas em critérios específicos) não
    são inseridas novamente.

    Args:
        request: O objeto HttpRequest que contém informações sobre a
                 requisição feita pelo usuário, incluindo o arquivo enviado.

    Returns:
        HttpResponse: Redireciona para a lista de vendas após o processamento
                       do arquivo, exibindo uma mensagem de sucesso ou erro
                       conforme o resultado da operação.

    Raises:
        Exception: Caso ocorra qualquer erro durante o processamento
        do arquivo, uma mensagem de erro será exibida ao usuário.

    Exemplo:
        Se um arquivo contendo as colunas CLIENTE, VENDEDOR, Código,
        Descrição do Produto/Serviço, Data, Vl. Unit., Vl. Total,
        Quantidade e Documento for carregado, as vendas serão processadas e
        inseridas no banco de dados, evitando duplicatas.
    """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file = request.FILES['file']  # Acessa o arquivo carregado

                # Usar a função de tratamento de dados
                df = tratar_dados(file)

                total_registros = len(df)
                print(total_registros)
                registros_inseridos = 0

                # Percorrer as linhas do DataFrame e processar os dados
                for index, row in df.iterrows():
                    # Garantir que o cliente exista
                    cliente_nome = row['CLIENTE']
                    cliente, created_cliente = Cliente.objects.get_or_create(
                        nome=cliente_nome
                    )

                    # Garantir que o vendedor exista
                    vendedor_nome = row['VENDEDOR']
                    vendedor, created_vendedor = (
                        Vendedor.objects.get_or_create(nome=vendedor_nome)
                    )

                    # Garantir que o produto exista
                    produto_codigo = row['CÓDIGO']
                    produto_nome = row['DESCRIÇÃO DO PRODUTO/SERVIÇO']
                    try:
                        produto, created = Produto.objects.get_or_create(
                            produto=produto_nome,
                            defaults={'codigo': produto_codigo},
                        )
                    except Exception as erro:
                        print(erro)
                        produto, created = Produto.objects.get_or_create(
                            produto=produto_nome, defaults={'codigo': None}
                        )

                    # Verifique se a venda já existe
                    venda_existente = Venda.objects.filter(
                        data_da_venda=row['DATA'],
                        cliente=cliente,
                        vendedor=vendedor,
                        produto=produto,
                        valor_total=row['VL. TOTAL'],
                        quantidade=row['QUANTIDADE'],
                        valor_unitario=row['VL. UNIT.'],
                        nf=row['DOCUMENTO'],
                    ).exists()

                    if not venda_existente:
                        # Criar a venda somente se ela não existir
                        Venda.objects.create(
                            data_da_venda=row['DATA'],
                            nf=row['DOCUMENTO'],
                            cliente=cliente,
                            vendedor=vendedor,
                            produto=produto,
                            unidade=row['UNID.'],
                            quantidade=row['QUANTIDADE'],
                            valor_unitario=row['VL. UNIT.'],
                            valor_total=row['VL. TOTAL'],
                        )
                        print(registros_inseridos)
                    else:
                        print('já existe')
                    registros_inseridos += 1
                messages.success(request, 'Arquivo importado com sucesso!')
                return redirect('vendas:lista_vendas')
            except Exception as e:
                print(f'{e}')
                messages.error(request, f'Erro ao processar o arquivo: {e}')
                return redirect('vendas:lista_vendas')
    else:
        form = UploadFileForm()
    return render(request, 'lista_vendas.html', {'form': form})


@login_required(login_url='/usuarios/login/')
def download_vendas(request):
    """
    Gera um arquivo Excel com os dados de vendas e permite o download.

    Esta view consulta as vendas no banco de dados e as exporta para um
    arquivo Excel ou CSV, que é retornado como resposta para download.

    Args:
        request: O objeto HttpRequest que contém informações
        sobre a requisição.

    Returns:
        HttpResponse: Um arquivo Excel ou CSV contendo os dados de vendas.
    """
    # Captura os filtros da URL
    vendedor = request.GET.get('vendedor', '')
    cliente = request.GET.get('cliente', '')

    # Consulta os dados das vendas
    vendas = Venda.objects.all().values(
        'data_da_venda',
        'nf',
        'cliente__nome',
        'vendedor__nome',
        'produto__codigo',
        'produto__produto',
        'unidade',
        'quantidade',
        'valor_unitario',
        'valor_total',
    )

    if vendedor:
        vendas = vendas.filter(vendedor__nome__icontains=vendedor)

    if cliente:
        vendas = vendas.filter(cliente__nome__icontains=cliente)
    # Cria um DataFrame a partir da QuerySet
    df = pd.DataFrame(vendas)

    # Renomeia as colunas para algo mais amigável (opcional)
    df.columns = [
        'Data da Venda',
        'Nota Fiscal',
        'Cliente',
        'Vendedor',
        'Código do Produto',
        'Nome do Produto',
        'Unidade',
        'Quantidade',
        'Valor Unitário',
        'Valor Total',
    ]

    # Gera o arquivo Excel em memória (usando o BytesIO)
    with io.BytesIO() as buffer:
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Vendas')
            writer.close()

        # Cria a resposta HTTP com o conteúdo do arquivo Excel
        response = HttpResponse(
            buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename="vendas.xlsx"'

    return response
