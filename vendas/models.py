from django.db import models
from django.urls import reverse_lazy

from clientes.models import Cliente
from produtos.models import Produto
from vendedores.models import Vendedor


class Venda(models.Model):
    """
    Representa uma venda no sistema.

    Attributes:
        data_da_venda (DateField): Data da venda realizada.
        nf (PositiveIntegerField): Número da Nota Fiscal, opcional.
        cliente (ForeignKey): Nome do cliente da venda.
        produto (ForeignKey): Nome do produto vendido.
        vendedor (ForeignKey): Vendedor responsável pela venda.
        quantidade (PositiveIntegerField): Quantidade de produto movimentada.

        unidade (str): Tipo da unidade do produto comercializado,
        se litro, balde, saca, kg...

        valor_unitario (Decimal): Preço unitário do produto com até 11 dígitos antes do
        ponto decimal e 2 dígitos após o ponto decimal.

        valor_total (Decimal): Preço total da venda com até 11 dígitos antes do
        ponto decimal e 2 dígitos após o ponto decimal.
    """

    data_da_venda = models.DateField()
    nf = models.PositiveIntegerField('Nota Fiscal', null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    unidade = models.CharField(max_length=20)
    quantidade = models.PositiveIntegerField()
    valor_unitario = models.DecimalField(
        'Valor Unitário', max_digits=11, decimal_places=2
    )
    valor_total = models.DecimalField(
        'Valor Total', max_digits=11, decimal_places=2
    )

    class Meta:
        """
        Metadados para o modelo Produto.

        Attributes:
            ordering (tuple): Define a ordenação padrão das instâncias
            de Venda. Os produtos serão ordenados pelo campo 'data_venda'
            em ordem decrescente (datas mais recentes primeiro).
        """

        ordering = ('-data_da_venda',)


    def __str__(self):
        """
        Retorna a representação em string da venda.

        Returns:
            str: O nome do cliente, vendedor e produto.
        """
        return f'{self.cliente} - {self.vendedor} - {self.produto}'
    

    def get_absolute_url(self):
        """
        Retorna a URL absoluta para o detalhe de uma venda específica.

        Returns:
            str: A URL para a visualização de detalhe da venda.
        """
        return reverse_lazy('produto:detalhe_produto', kwargs={'pk': self.pk})
    

    def dict_to_json(self):
        """
        Retorna um dicionário representando os dados da venda
        para conversão em JSON.

        Este método é utilizado para serializar os dados principais
        da venda em um formato de dicionário, adequado para
        conversão em JSON, facilitando a integração com APIs ou
        outras funcionalidades que requeiram dados em formato JSON.

        Returns:
            dict: Um dicionário contendo o identificador primário (pk),
            e os dados da venda.
        """
        return {
            'pk': self.pk,
            'cliente': str(self.cliente),
            'vendedor': str(self.vendedor),
            'produto': str(self.produto),
            'quantidade': self.quantidade,
            'valor_unitario': str(self.valor_unitario),
            'valor_total': str(self.valor_total),
            'data_venda': self.data_da_venda.isoformat(),
        }
