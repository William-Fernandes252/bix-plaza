import uuid


from django.db import models


class Address(models.Model):
    """Model for Address."""

    class UfChoices(models.TextChoices):
        """Enum for UF choices."""

        AC = "AC", "Acre"
        AL = "AL", "Alagoas"
        AP = "AP", "Amapá"
        AM = "AM", "Amazonas"
        BA = "BA", "Bahia"
        CE = "CE", "Ceará"
        DF = "DF", "Distrito Federal"
        ES = "ES", "Espírito Santo"
        GO = "GO", "Goiás"
        MA = "MA", "Maranhão"
        MT = "MT", "Mato Grosso"
        MS = "MS", "Mato Grosso do Sul"
        MG = "MG", "Minas Gerais"
        PA = "PA", "Pará"
        PB = "PB", "Paraíba"
        PR = "PR", "Paraná"
        PE = "PE", "Pernambuco"
        PI = "PI", "Piauí"
        RJ = "RJ", "Rio de Janeiro"
        RN = "RN", "Rio Grande do Norte"
        RS = "RS", "Rio Grande do Sul"
        RO = "RO", "Rondônia"
        RR = "RR", "Roraima"
        SC = "SC", "Santa Catarina"
        SP = "SP", "São Paulo"
        SE = "SE", "Sergipe"
        TO = "TO", "Tocantins"

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    uf = models.CharField(max_length=2, choices=UfChoices.choices)
    zip_code = models.CharField(max_length=8, unique=True)

    class Meta:
        """Meta options for Address."""

        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self) -> str:
        """Return the string representation of the address."""
        return self.street
