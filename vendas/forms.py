from django import forms

from .models import Venda


class VendaForm(forms.ModelForm):
    """
    Formulário para criação e atualização de objetos do modelo Venda.

    Este formulário é baseado no modelo Venda e inclui 
    todos os campos do modelo.
    """

    class Meta:
        """
        Metadados para o formulário VendaForm.

        Atributos:
            model (Model): O modelo que será utilizado neste formulário.
            fields (str or list): Os campos do modelo a serem 
            incluídos no formulário.
        """
        
        # Define o modelo que será utilizado no formulário, 
        # que neste caso é o Venda
        model = Venda
        fields = '__all__' # Inclui todos os campos do modelo Venda
    

