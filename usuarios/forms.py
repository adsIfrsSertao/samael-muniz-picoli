from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Formulário personalizado para a criação de usuários.

    Este formulário estende o UserCreationForm padrão do Django para
    incluir rótulos personalizados para os campos de senha e para
    adicionar validação única ao nome de usuário.

    Attributes:
        Meta: Classe interna que define o modelo e os campos do formulário.
    """

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        

    def __init__(self, *args, **kwargs):
        """
        Inicializa o formulário e personaliza os rótulos dos campos de senha.

        Args:
            *args: Argumentos posicionais.
            **kwargs: Argumentos nomeados.
        """
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirme a Senha'


    def clean_username(self):
        """
        Verifica se o nome de usuário já está em uso.

        Se o nome de usuário fornecido já existir no banco de dados,
        uma exceção de validação é levantada.

        Returns:
            str: O nome de usuário limpo se for único.

        Raises:
            forms.ValidationError: Se o nome de usuário já estiver em uso.
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Esse nome de usuário já está em uso. Escolha outro, por favor.'
            )
        return username
