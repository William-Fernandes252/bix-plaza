import pytest
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from tests.test_users.factories import UserFactory

from hotels import models


class DescribeHotel:
    class DescribeSave:
        def it_raises_validation_error_if_manager_is_not_in_manager_group(
            self, hotel: models.Hotel, faker
        ):
            with pytest.raises(ValidationError):
                hotel.manager = UserFactory.create(email=faker.email())
                hotel.save()

        def it_does_not_raise_validation_error_if_manager_is_in_manager_group(
            self, hotel: models.Hotel
        ):
            hotel.manager.groups.add(
                Group.objects.get(name=models.Group.MANAGERS.value)
            )

    class DescribeGetAbsoluteUrl:
        def it_returns_the_absolute_url(self, hotel: models.Hotel):
            assert hotel.get_absolute_url() == f"/hotels/{hotel.pk}/"

    class DescribeStr:
        def it_returns_the_hotel_name_and_address(self, hotel: models.Hotel):
            assert str(hotel) == f"{hotel.name} ({hotel.address})"


class DescribeRoom:
    class DescribeGetAbsoluteUrl:
        def it_returns_the_absolute_url(self, room: models.Room):
            assert room.get_absolute_url() == f"/rooms/{room.pk}/"

    class DescribeStr:
        def it_returns_the_room_number_and_hotel_name(self, room: models.Room):
            assert str(room) == f"{room.number} - {room.hotel} - {room.room_type}"

    class DescribeCheckIn:
        def it_sets_the_room_status_to_occupied(self, room: models.Room):
            room.check_in()
            assert room.occupied is True

        def it_raises_validation_error_if_room_is_occupied(self, room: models.Room):
            room.occupied = True
            with pytest.raises(ValidationError):
                room.check_in()

    class DescribeCheckOut:
        @pytest.fixture
        def occupied_room(self, room: models.Room):
            room.check_in()
            return room

        def it_sets_the_room_status_to_vacant(self, occupied_room: models.Room):
            occupied_room.check_out()
            assert occupied_room.occupied is False

        def it_raises_validation_error_if_room_is_vacant(
            self, occupied_room: models.Room
        ):
            occupied_room.occupied = False
            with pytest.raises(ValidationError):
                occupied_room.check_out()
