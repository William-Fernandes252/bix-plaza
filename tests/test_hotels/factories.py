from typing import Iterable

from django.contrib.auth.models import Group as AuthGroup
from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory, DjangoOptions
from factory.fuzzy import FuzzyChoice, FuzzyFloat
from faker import Faker

from hotels import models
from tests.test_addresses.factories import AddressFactory
from tests.test_users.factories import UserFactory
from users.models import Group

faker = Faker("en_US")


class HotelFactory(DjangoModelFactory):
    name = faker.company()
    email = faker.email()
    phone_number = faker.phone_number()
    manager = SubFactory(
        UserFactory,
        groups=AuthGroup.objects.filter(name=Group.MANAGERS.value),
        email=faker.email(),
    )
    owner = SubFactory(UserFactory)
    address = SubFactory(AddressFactory)

    class Meta(DjangoOptions):
        model = models.Hotel
        django_get_or_create = ("manager",)

    @post_generation
    def rooms(
        self: models.Hotel, create: bool, extracted: Iterable[models.Room], **kwargs
    ):
        if create and extracted:
            self.rooms.set(extracted)


class RoomFactory(DjangoModelFactory):
    class Meta(DjangoOptions):
        model = models.Room

    hotel = SubFactory(HotelFactory)
    number = faker.random_number(3)
    price = FuzzyFloat(100, 1000)
    floor = faker.random_number(2)
    room_type = FuzzyChoice(models.Room.RoomType.values)

    @post_generation
    def bookings(
        self: models.Room, create: bool, extracted: Iterable[models.Booking], **kwargs
    ):
        if create and extracted:
            self.bookings.set(extracted)
