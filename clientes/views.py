from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy

from .forms import ClienteForm
from .models import Cliente


# Create your views here.
class ClientesList(ListView):
    """
    Classe-based view para listar Cliente.
    
    Attributes:
        model (Model): O modelo que será utilizado na listagem.
        template_name (str): O nome do template que será renderizado.
        paginate_by (int): Quantidade de itens por página na paginação.
    """
    model = Cliente
    template_name = 'lista_cliente.html'
    paginate_by = 3
    context_object_name = 'clientes'


class CriarCliente(CreateView):
    """
    View baseada em classe para criar um novo Cliente.

    Attributes:
        model (Model): O modelo que será utilizado na view.
        template_name (str): O nome do template que será renderizado.
        form_class (Form): O formulário que será utilizado 
        para criar o objeto.
        success_url (Django.Url): Página que será direcionada após a conclusão.
    """
    model = Cliente
    template_name = 'formulario_cliente.html'
    form_class = ClienteForm
    success_url = reverse_lazy('clientes:lista_cliente')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente inserido com sucesso!')
        return super().form_valid(form)
    

class EditarCliente(UpdateView):
    """
    View baseada em classe para editar um cliente.

    Attributes:
        model (Model): O modelo que será utilizado na view.
        template_name (str): O nome do template que será renderizado.
        form_class (Form): O formulário que será utilizado 
        para criar o objeto.
        success_url (Django.Url): Página que será direcionada após a conclusão.
    """
    model = Cliente
    template_name = 'formulario_cliente.html'
    form_class = ClienteForm
    success_url = reverse_lazy('clientes:lista_cliente')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente atualizado com sucesso!')
        return super().form_valid(form)


class DeletarCliente(DeleteView):
    """
    View baseada em classe para deletar um cliente.

    Attributes:
        model (Model): O modelo que será utilizado na view.
        success_url (Django.Url): Página que será direcionada após a conclusão.
    """
    model = Cliente
    success_url = reverse_lazy('clientes:lista_cliente')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Cliente removido com sucesso!')
        return super().delete(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def cliente_json(request, pk):
    """
    Retorna os dados de um cliente específico em formato JSON.

    Este método filtra o cliente com base na chave primária 
    fornecida (pk), converte os dados principais do cliente 
    em um formato de dicionário utilizando o método `dict_to_json`
    e retorna os dados como uma resposta JSON.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        pk (int): A chave primária do cliente a ser recuperado.

    Returns:
        JsonResponse: Um objeto de resposta JSON contendo os 
        dados do cliente.
    """
    cliente = get_object_or_404(Cliente, pk=pk)
    data = cliente.dict_to_json()
    return JsonResponse({'data': data})
   



