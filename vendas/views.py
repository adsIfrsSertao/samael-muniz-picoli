from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import formats
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import VendaForm
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
    paginate_by = 3
    context_object_name = 'vendas'


@login_required(login_url='/usuarios/login/')
def detalhe_venda(request, pk):
    """
    View para exibir os detalhes de um Venda específico.

    Args:
        request (HttpRequest): O objeto de solicitação HTTP.
        pk (int): A chave primária do Venda a ser exibido.

    Returns:
        HttpResponse: A resposta HTTP com o template
        `detalhe_Venda.html` renderizado.
    """
    nome_template = 'detalhe_venda.html'

    # Recupera o objeto Venda com a chave primária fornecida
    obj = get_object_or_404(Venda, pk=pk)

    # Define o contexto a ser passado para o template
    contexto = {'objeto': obj}

    # Renderiza o template com o contexto
    return render(request, template_name=nome_template, context=contexto)


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
        context['venda'].valor_unitario = "{:.2f}".format(venda.valor_unitario).replace(',', '.')
        context['venda'].valor_total = "{:.2f}".format(venda.valor_total).replace(',', '.')
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
