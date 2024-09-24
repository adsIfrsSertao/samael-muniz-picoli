from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from usuarios.forms import CustomUserCreationForm

class CadastrarUsuario(UserPassesTestMixin, CreateView):
    """
    View para cadastrar um novo usuário.

    Esta view permite que apenas superadministradores cadastrem
    novos usuários utilizando um formulário personalizado.

    Attributes:
        model: O modelo de usuário a ser utilizado.
        form_class: O formulário usado para criar um novo usuário.
        template_name: O template a ser renderizado para o cadastro.
        success_url: A URL para redirecionar após o cadastro bem-sucedido.
    """
    model = User
    form_class = CustomUserCreationForm
    template_name = 'cadastro.html'
    success_url = reverse_lazy('usuarios:login')

    def test_func(self):
        """
        Verifica se o usuário atual é um superadministrador.

        Returns:
            bool: Retorna True se o usuário for um superadministrador,
            caso contrário, retorna False.
        """
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Redireciona usuários não autorizados para a página inicial.

        Caso o usuário não tenha permissão para acessar esta view,
        ele é redirecionado para a URL especificada.
        
        Returns:
            HttpResponse: Redireciona para a página inicial.
        """
        return redirect('core:index') 


class CustomLoginView(LoginView):
    """
    View personalizada para o login de usuários.

    Esta view estende a LoginView padrão do Django e personaliza
    o comportamento de exibição de erros e redirecionamento para
    usuários já autenticados.

    Attributes:
        template_name: O template a ser renderizado para o login.
        success_url: A URL para redirecionar após um login bem-sucedido.
    """
    template_name = 'login.html'
    success_url = reverse_lazy('core:index')

    def form_invalid(self, form):
        """
        Manipula a situação em que o formulário de login é inválido.

        Remove mensagens de erro padrão e adiciona uma mensagem de erro
        personalizada ao formulário.

        Args:
            form: O formulário de login que falhou na validação.

        Returns:
            HttpResponse: Retorna a resposta renderizada com o formulário.
        """
        form.errors.clear()
        form.add_error(None, 'Senha ou usuário inválido.')
        return super().form_invalid(form)
    
    def get(self, request, *args, **kwargs):
        """
        Manipula solicitações GET para a view de login.

        Redireciona usuários já autenticados para a página inicial,
        em vez de exibir a página de login.

        Args:
            request: A solicitação HTTP.
            *args: Argumentos posicionais adicionais.
            **kwargs: Argumentos nomeados adicionais.

        Returns:
            HttpResponse: Redireciona para a página inicial se o usuário
            estiver autenticado, ou renderiza a página de login.
        """
        if request.user.is_authenticated:
            return redirect('core:index')  # Redireciona para a página inicial
        return super().get(request, *args, **kwargs)
