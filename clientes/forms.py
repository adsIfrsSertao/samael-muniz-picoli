from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    """
    Formulário para criação e atualização de objetos do modelo Cliente.

    Este formulário é baseado no modelo cliente e inclui
    todos os campos do modelo.
    """

    class Meta:
        """
        Metadados para o formulário ClienteForm.

        Atributos:
            model (Model): O modelo que será utilizado neste formulário.
            fields (str or list): Os campos do modelo a serem
            incluídos no formulário.
        """

        model = Cliente
        fields = '__all__'
