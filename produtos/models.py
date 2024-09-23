from django.db import models
from django.urls import reverse_lazy

# Create your models here.

class Produto(models.Model):

    """
    Representa um produto no sistema

    Attributes:
        produto (str): Nome do produto, deve ser único.
    """
    produto = models.CharField(max_length=100, unique=True, null=False)
    codigo = models.CharField(max_length=100, unique=True, null=True, blank=True)

    class Meta:
        """
        Metadados para o modelo Produto.

        Attributes:
            ordering (tuple): Define a ordenação padrão das instâncias
            de Produto. No caso, os produtos serão ordenados pelo 
            campo 'produto' em ordem alfabética.

        """
        ordering = ('produto',)

    def __str__(self):
        """
        Retorna a representação em string do produto.

        Returns:
            str: O nome do produto.
        """
        return f'{self.produto}'
    

    def dict_to_json(self):
        """
        Retorna um dicionário representando os dados do produto
        para conversão em JSON.

        Este método é utilizado para serializar os dados principais
        do produto em um formato de dicionário, adequado para 
        conversão em JSON, facilitando a integração com APIs ou 
        outras funcionalidades que requeiram dados em formato JSON.

        Returns:
            dict: Um dicionário contendo o identificador primário (pk), 
            e o nome do produto.
        """
        return {
            'pk': self.pk,
            'produto': self.produto,
        }
    
    def get_absolute_url(self):
        """
        Retorna a URL absoluta para o detalhe de um produto específico.
        
        Returns:
            str: A URL para a visualização de detalhe do produto.
        """
        return reverse_lazy('produtos:detalhe_produto', kwargs={'pk':self.pk})