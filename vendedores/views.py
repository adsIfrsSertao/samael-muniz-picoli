from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy

from .forms import VendedorForm
from .models import Vendedor


class VendedoresList(LoginRequiredMixin, ListView):
    """
    Classe-based view para listar vendedor.
    
    Atributos:
        model (Model): O modelo que será utilizado na listagem.
        template_name (str): O nome do template que será renderizado.
        paginate_by (int): Quantidade de itens por página na paginação.
    """
    model = Vendedor
    template_name = 'lista_vendedor.html'
    paginate_by = 3
    context_object_name = 'vendedores'



class CriarVendedor(LoginRequiredMixin, CreateView):
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
        messages.success(self.request, 'Vendedor inserido com sucesso!')
        return super().form_valid(form)
    


class EditarVendedor(LoginRequiredMixin, UpdateView):
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
        messages.success(self.request, 'Vendedor atualizado com sucesso!')
        return super().form_valid(form)



class DeletarVendedor(LoginRequiredMixin, DeleteView):
    """
    View baseada em classe para deletar um vendedor.

    Attributes:
        model (Model): O modelo que será utilizado na view.
        success_url (Django.Url): Página que será direcionada após a conclusão.
    """
    model = Vendedor
    success_url = reverse_lazy('vendedores:lista_vendedores')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'vendedor removido com sucesso!')
        return super().delete(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required(login_url='/usuarios/login/')
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
   


