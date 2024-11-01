from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import VendedorForm
from .models import Vendedor


class SuperAdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin que exige que o usuário seja superadministrador.

    Este mixin eleva um erro 404 se o usuário autenticado não for um
    superadministrador.
    """

    def test_func(self):
        """
        Verifica se o usuário é um superadministrador.

        Returns:
            bool: True se o usuário for superadministrador,
                  caso contrário, levanta um Http404.
        """

        if not self.request.user.is_superuser:
            raise Http404('Página não encontrada')
        return True


class VendedoresList(SuperAdminRequiredMixin, LoginRequiredMixin, ListView):
    """
    Classe-based view para listar vendedor.

    Atributos:
        model (Model): O modelo que será utilizado na listagem.
        template_name (str): O nome do template que será renderizado.
        paginate_by (int): Quantidade de itens por página na paginação.
    """

    model = Vendedor
    template_name = 'lista_vendedor.html'
    paginate_by = 10
    context_object_name = 'vendedores'

    def get_queryset(self):
        """
        Retorna o conjunto de consultas para a listagem de vendedores.

        O método filtra os vendedores com base no parâmetro de busca 'nome'
        fornecido na requisição GET. Se o parâmetro estiver presente e não
        for vazio, o queryset será filtrado para incluir apenas os vendedores
        cujo nome contém o valor fornecido.

        Returns:
            QuerySet: O conjunto de vendedores filtrado.
        """

        queryset = super().get_queryset()
        vendedor = self.request.GET.get('vendedor', '')
        if vendedor:
            queryset = queryset.filter(nome__icontains=vendedor)

        return queryset


class CriarVendedor(SuperAdminRequiredMixin, LoginRequiredMixin, CreateView):
    """
    View baseada em classe para criar um novo vendedor.

    Atributos:
        model (Model): O modelo que será utilizado na view.
        template_name (str): O nome do template que será renderizado.
        form_class (Form): O formulário que será utilizado
        para criar o objeto.
    """

    model = Vendedor
    template_name = 'formulario_vendedor.html'
    form_class = VendedorForm
    success_url = reverse_lazy('vendedores:lista_vendedores')

    def form_valid(self, form):
        """
        Processa o formulário quando é válido.

        Adiciona uma mensagem de sucesso e chama o método pai.

        Args:
            form (Form): O formulário com os dados do vendedor.

        Returns:
            HttpResponse: Resposta redirecionando para a URL de sucesso.
        """

        messages.success(self.request, 'Vendedor inserido com sucesso!')
        return super().form_valid(form)


class EditarVendedor(SuperAdminRequiredMixin, LoginRequiredMixin, UpdateView):
    """
    View baseada em classe para editar um vendedor.

    Atributos:
        model (Model): O modelo que será utilizado na view.
        template_name (str): O nome do template que será renderizado.
        form_class (Form): O formulário que será utilizado
        para criar o objeto.
    """

    model = Vendedor
    template_name = 'formulario_vendedor.html'
    form_class = VendedorForm
    success_url = reverse_lazy('vendedores:lista_vendedores')

    def form_valid(self, form):
        """
        Processa o formulário quando é válido.

        Adiciona uma mensagem de sucesso e chama o método pai.

        Args:
            form (Form): O formulário com os dados atualizados do vendedor.

        Returns:
            HttpResponse: Resposta redirecionando para a URL de sucesso.
        """

        messages.success(self.request, 'Vendedor atualizado com sucesso!')
        return super().form_valid(form)


class DeletarVendedor(SuperAdminRequiredMixin, LoginRequiredMixin, DeleteView):
    """
    View baseada em classe para deletar um vendedor.

    Attributes:
        model (Model): O modelo que será utilizado na view.
        success_url (Django.Url): Página que será direcionada após a conclusão.
    """

    model = Vendedor
    success_url = reverse_lazy('vendedores:lista_vendedores')

    def delete(self, request, *args, **kwargs):
        """
        Processa a solicitação de exclusão de um vendedor.

        Adiciona uma mensagem de sucesso e chama o método pai.

        Args:
            request (HttpRequest): O objeto de requisição HTTP.
            *args: Argumentos adicionais.
            **kwargs: Argumentos adicionais.

        Returns:
            HttpResponse: Resposta redirecionando para a URL de sucesso.
        """

        messages.success(self.request, 'vendedor removido com sucesso!')
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Redireciona a solicitação GET para o método POST.

        Args:
            request (HttpRequest): O objeto de requisição HTTP.
            *args: Argumentos adicionais.
            **kwargs: Argumentos adicionais.

        Returns:
            HttpResponse: Resposta da solicitação POST.
        """

        return self.post(request, *args, **kwargs)


@login_required(login_url='/usuarios/login/')
@user_passes_test(lambda u: u.is_superuser, redirect_field_name=None)
def vendedor_json(request, pk):
    """
    Retorna os dados de um vendedor específico em formato JSON.

    Este método filtra o vendedor com base na chave primária
    fornecida (pk), converte os dados principais do vendedor
    em um formato de dicionário utilizando o método `dict_to_json`
    e retorna os dados como uma resposta JSON.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        pk (int): A chave primária do vendedor a ser recuperado.

    Returns:
        JsonResponse: Um objeto de resposta JSON contendo os
        dados do vendedor.
    """
    vendedor = get_object_or_404(Vendedor, pk=pk)
    data = vendedor.dict_to_json()
    return JsonResponse({'data': data})
