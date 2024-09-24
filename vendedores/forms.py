from django import forms

from .models import Vendedor


class VendedorForm(forms.ModelForm):
    """
    Formulário para criação e atualização de objetos do modelo Vendedor.

    Este formulário é baseado no modelo Vendedor e inclui
    todos os campos do modelo.
    """

    class Meta:
        """
        Metadados para o formulário VendedorForm.

        Atributos:
            model (Model): O modelo que será utilizado neste formulário.
            fields (str or list): Os campos do modelo a serem
            incluídos no formulário.
        """

        model = Vendedor
        fields = '__all__'
