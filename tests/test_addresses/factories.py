from factory.django import DjangoModelFactory, DjangoOptions
from factory.fuzzy import FuzzyChoice
from faker import Faker

from addresses.models import Address

faker = Faker("pt_BR")


class AddressFactory(DjangoModelFactory):
    city = faker.city()
    neighborhood = faker.bairro()
    uf = FuzzyChoice(choices=Address.UfChoices.values)
    street = faker.street_name()
    zip_code = faker.postcode(formatted=False)

    class Meta(DjangoOptions):
        model = Address
        django_get_or_create = ("zip_code",)
