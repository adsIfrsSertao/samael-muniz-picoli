from django.db import models

# Create your models here.


class TimeStampModel(models.Model):
    """
    Modelo abstrato que fornece campos de data/hora para
    criação e última atualização.

    Attributes:
        criado_em (DateTimeField): Armazena a data e hora em
        que a instância foi criada.
        Preenchido automaticamente na criação.

        atualizado_em (DateTimeField): Armazena a data e hora da
        última atualização da instância. Atualizado automaticamente
        cada vez que a instância é salva.
    """

    criado_em = models.DateTimeField(
        'criado_em', auto_now_add=True, auto_now=False
    )

    atualizado_em = models.DateTimeField(
        'atualizado_em', auto_now_add=False, auto_now=True
    )

    class Meta:
        """
        Metadados para o modelo TimeStampModel.

        Attributes:
            abstract (bool): Se verdadeiro, indica que o modelo é
            abstrato e não será criado no banco de dados. (Opcional)
        """

        abstract = True
