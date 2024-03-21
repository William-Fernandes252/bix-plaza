import pytest

from hotels import models
from tests.test_hotels import factories


@pytest.fixture
def room(db) -> models.Room:
    """Return a room instance."""
    return factories.RoomFactory()


@pytest.fixture
def hotel(db) -> models.Hotel:
    """Return a hotel instance."""
    return factories.HotelFactory(rooms=[factories.RoomFactory() for _ in range(3)])
