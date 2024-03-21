import pytest

from tests.test_bookings.factories import BookingFactory


@pytest.fixture
def booking(db):
    """Create a booking."""
    return BookingFactory.create()
