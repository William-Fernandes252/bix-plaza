from datetime import timedelta

from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory, DjangoOptions
from faker import Faker

from hotels import models
from tests.test_hotels import factories
from tests.test_users.factories import UserFactory

faker = Faker("en_US")


class BookingFactory(DjangoModelFactory):
    class Meta(DjangoOptions):
        model = models.Booking

    room = SubFactory(factories.RoomFactory)
    client = SubFactory(UserFactory)
    start = faker.date_object()
    end = LazyAttribute(lambda o: o.start + timedelta(days=5))
