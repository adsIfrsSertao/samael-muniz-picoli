from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ProdutoForm
from .models import Produto


class ProdutoList(LoginRequiredMixin, ListView):
    """
    Classe-based view para listar produtos.

    Atributos:
        model (Model): O modelo que será utilizado na listagem.
        template_name (str): O nome do template que será renderizado.
        paginate_by (int): Quantidade de itens por página na paginação.
    """

    model = Produto
    template_name = 'lista_produtos.html'
    paginate_by = 10
    context_object_name = 'produtos'

    def get_queryset(self):
        """
        Retorna o conjunto de consultas para a listagem de produtos.

        O método filtra os produtos com base no parâmetro de busca 'produto'
        fornecido na requisição GET. Se o parâmetro estiver presente e não
        for vazio, o queryset será filtrado para incluir apenas os produtos
        cujo nome contém o valor fornecido.

        Returns:
            QuerySet: O conjunto de produtos filtrado.
        """

        queryset = super().get_queryset()
        produto = self.request.GET.get('produto', '')
        if produto:
            queryset = queryset.filter(produto__icontains=produto)

        return queryset


class CriarProduto(LoginRequiredMixin, CreateView):
    """
    View baseada em classe para criar um novo produto.

    Atributos:
        model (Model): O modelo que será utilizado na view.
        template_name (str): O nome do template que será renderizado.
        form_class (Form): O formulário que será utilizado
        para criar o objeto.
    """

    model = Produto
    template_name = 'formulario_produto.html'
    form_class = ProdutoForm
    success_url = reverse_lazy('produtos:lista_produtos')

    def form_valid(self, form):
        messages.success(self.request, 'Produto inserido com sucesso!')
        return super().form_valid(form)


class EditarProduto(LoginRequiredMixin, UpdateView):
    """
    View baseada em classe para editar um produto.

    Atributos:
        model (Model): O modelo que será utilizado na view.
        template_name (str): O nome do template que será renderizado.
        form_class (Form): O formulário que será utilizado
        para criar o objeto.
    """

    model = Produto
    template_name = 'formulario_produto.html'
    form_class = ProdutoForm
    success_url = reverse_lazy('produtos:lista_produtos')

    def form_valid(self, form):
        messages.success(self.request, 'Produto atualizado com sucesso!')
        return super().form_valid(form)


class DeletarProduto(LoginRequiredMixin, DeleteView):
    """
    View baseada em classe para deletar um produto.

    Attributes:
        model (Model): O modelo que será utilizado na view.
        success_url (Django.Url): Página que será direcionada após a conclusão.
    """

    model = Produto
    success_url = reverse_lazy('produtos:lista_produtos')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Produto removido com sucesso!')
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required(login_url='usuarios/login/')
def produto_json(request, pk):
    """
    Retorna os dados de um produto específico em formato JSON.

    Este método filtra o produto com base na chave primária
    fornecida (pk), converte os dados principais do produto
    em um formato de dicionário utilizando o método `dict_to_json`
    e retorna os dados como uma resposta JSON.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        pk (int): A chave primária do produto a ser recuperado.

    Returns:
        JsonResponse: Um objeto de resposta JSON contendo os
        dados do produto.
    """
    produto = get_object_or_404(Produto, pk=pk)
    data = produto.dict_to_json()
    return JsonResponse({'data': data})
