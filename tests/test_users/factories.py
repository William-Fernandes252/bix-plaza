from typing import Iterable

from django.contrib.auth.models import Group
from factory import post_generation
from factory.django import DjangoModelFactory, DjangoOptions
from faker import Faker

from users.models import User

faker = Faker("en_US")


class UserFactory(DjangoModelFactory):
    class Meta(DjangoOptions):
        model = User
        django_get_or_create = ("email",)

    email = faker.email()
    is_active = True
    name = faker.name()
    phone_number = faker.msisdn()

    @post_generation
    def password(self: User, create: bool, extracted: str, **kwargs):  # noqa: FBT001
        if create:
            password = extracted if extracted else faker.password(20)
            self.set_password(password)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """Save again the instance if creating and at least one hook ran."""
        if create and results and not cls._meta.skip_postgeneration_save:
            instance.save()

    @post_generation
    def groups(self: User, create, extracted: Iterable[Group], **kwargs):
        if create and extracted:
            self.groups.set(extracted)
