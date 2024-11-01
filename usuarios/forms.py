from django import forms
from django.contrib.auth import password_validation
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

    is_staff_or_superuser = forms.BooleanField(
        required=False,
        label="Conceder permissões de superusuário e membro da equipe",
        help_text="Marque esta opção para conceder permissões de administrador e membro da equipe ao usuário."
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'is_staff_or_superuser')
        

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
    

class CustomPasswordChangeForm(forms.Form):
    """
    Formulário personalizado para alteração de senha, permitindo que o usuário
    defina uma nova senha sem a necessidade de informar a senha antiga.

    Este formulário inclui validações para garantir que a nova senha
    atenda aos critérios de segurança definidos e que as duas entradas 
    de senha coincidam.
    """
    new_password1 = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Confirme a nova senha",
        widget=forms.PasswordInput,
    )

    def clean_new_password2(self):
        """
        Valida o segundo campo de senha para garantir que ele corresponda
        ao primeiro campo de senha e que atenda aos critérios de segurança.

        Raises:
            ValidationError: Se as senhas não coincidirem ou não atenderem
            aos critérios de segurança.

        Returns:
            str: A nova senha confirmada se a validação for bem-sucedida.
        """
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        password_validation.validate_password(password2)
        return password2

    def save(self, user):
        """
        Salva a nova senha no usuário especificado.

        Este método define a nova senha para o usuário e salva as alterações.

        Args:
            user (User): O objeto do usuário cuja senha será alterada.
        """
        user.set_password(self.cleaned_data["new_password1"])
        user.save()
