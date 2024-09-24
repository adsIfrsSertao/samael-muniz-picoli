from django.db import models

# Create your models here.
class Cliente(models.Model):
    """
    Representa um cliente no sistema.

    Attributes:
        nome (str): Nome do cliente, deve ser único e não pode ser nulo.
    """

    nome = models.CharField(max_length=100, unique=True, null=False)

    class Meta:
        """
        Metadados para o modelo Cliente.

        Attributes:
            ordering (tuple): Define a ordenação padrão das instâncias
            de Cliente. No caso, os clientes serão ordenados pelo
            campo 'nome' em ordem alfabética.

        """

        ordering = ('nome',)

    def __str__(self):
        """
        Retorna a representação em string do cliente.

        Returns:
            str: O nome do cliente.
        """
        return f'{self.nome}'

    def dict_to_json(self):
        """
        Retorna um dicionário representando os dados do cliente
        para conversão em JSON.

        Este método é utilizado para serializar os dados do cliente
        em um formato de dicionário, adequado para
        conversão em JSON, facilitando a integração com APIs ou
        outras funcionalidades que requeiram dados em formato JSON.

        Returns:
            dict: Um dicionário contendo o identificador primário (pk),
            e o nome do cliente.
        """
        return {
            'pk': self.pk,
            'cliente': self.nome,
        }
