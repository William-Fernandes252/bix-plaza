from datetime import date
from typing import Self

from django.db import models

from bookings.models import Booking


class RoomQuerySet(models.QuerySet):
    def available(self, start: date, end: date) -> Self:
        """Return available rooms for the given period."""
        return self.exclude(
            id__in=Booking.objects.filter(
                models.Q(start__lte=start, end__gte=start)
                | models.Q(start__lte=end, end__gte=end)
            ),
            status__in=[
                Booking.StatusChoices.CHECKED_OUT,
                Booking.StatusChoices.CANCELED,
                Booking.StatusChoices.PENDING,
            ],
        )
