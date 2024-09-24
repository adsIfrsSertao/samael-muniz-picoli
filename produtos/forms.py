from django import forms

from .models import Produto


class ProdutoForm(forms.ModelForm):
    """
    Formulário para criação e atualização de objetos do modelo Produto.

    Este formulário é baseado no modelo Produto e inclui
    todos os campos do modelo.
    """

    class Meta:
        """
        Metadados para o formulário ProdutoForm.

        Atributos:
            model (Model): O modelo que será utilizado neste formulário.
            fields (str or list): Os campos do modelo a serem
            incluídos no formulário.
        """

        model = Produto
        fields = '__all__'  # Inclui todos os campos do modelo Produto
