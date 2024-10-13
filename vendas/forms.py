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

        model = Venda
        fields = '__all__'


    def clean_quantidade(self):
        """
        Valida o campo 'quantidade'.

        Verifica se a quantidade informada é pelo menos 1. Se a quantidade for menor
        que 1, uma ValidationError é levantada com uma mensagem apropriada.

        Returns:
            int: A quantidade informada, se válida.

        Raises:
            forms.ValidationError: Se a quantidade for menor que 1.
        """

        quantidade = self.cleaned_data.get('quantidade')
        if quantidade < 1:
            raise forms.ValidationError("A quantidade deve ser pelo menos 1.")
        return quantidade
    

    def clean_valor_unitario(self):
        """
        Valida o campo 'valor_unitario'.

        Verifica se o valor unitário informado é pelo menos 0.1. Se o valor unitário
        for menor que 0.1, uma ValidationError é levantada com uma mensagem apropriada.

        Returns:
            float: O valor unitário informado, se válido.

        Raises:
            forms.ValidationError: Se o valor unitário for menor que 0.1.
        """

        valor_unitario = self.cleaned_data.get('valor_unitario')
        if valor_unitario < 0.1:
            raise forms.ValidationError(
                "O valor unitário deve ser pelo menos 0.1.")
        return valor_unitario
    

    def clean_valor_total(self):
        """
        Valida o campo 'valor_total'.

        Verifica se o valor total informado é pelo menos 0.1. Se o valor total
        for menor que 0.1, uma ValidationError é levantada com uma mensagem apropriada.

        Returns:
            float: O valor total informado, se válido.

        Raises:
            forms.ValidationError: Se o valor total for menor que 0.1.
        """

        valor_total = self.cleaned_data.get('valor_total')
        if valor_total < 0.1:
            raise forms.ValidationError(
                "O valor unitário deve ser pelo menos 0.1.")
        return valor_total
    

class UploadFileForm(forms.Form):
    """
    Formulário para upload de arquivos.

    Este formulário permite que o usuário faça o upload de um arquivo,
    utilizando um campo de arquivo.
    """
    file = forms.FileField()
