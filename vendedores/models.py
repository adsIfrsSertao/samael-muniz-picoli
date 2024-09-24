from django.db import models

# Create your models here.


class Vendedor(models.Model):
    """
    Representa um vendedor no sistema.

    Attributes:
        nome (str): Nome do vendedor, deve ser único.
    """

    nome = models.CharField(max_length=100, unique=True, null=False)

    class Meta:
        """
        Metadados para o modelo Vendedor.

        Attributes:
            ordering (tuple): Define a ordenação padrão das instâncias
            de Vendedor. No caso, os vendedores serão ordenados pelo
            campo 'nome' em ordem crescente.

        """

        ordering = ('nome',)

    def __str__(self):
        """
        Retorna a representação em string do Vendedor.

        Returns:
            str: O nome do Vendedor.
        """
        return f'{self.nome}'

    def dict_to_json(self):
        """
        Retorna um dicionário representando os dados do Vendedor
        para conversão em JSON.

        Este método é utilizado para serializar os dados do Vendedor
        em um formato de dicionário, adequado para
        conversão em JSON, facilitando a integração com APIs ou
        outras funcionalidades que requeiram dados em formato JSON.

        Returns:
            dict: Um dicionário contendo o identificador primário (pk),
            e o nome do Vendedor.
        """
        return {
            'pk': self.pk,
            'vendedor': self.nome,
        }
