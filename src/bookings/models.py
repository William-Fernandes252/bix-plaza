import uuid
from datetime import date
from typing import ClassVar, Self

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from django_fsm import FSMField, transition


class BookingQuerySet(models.QuerySet):
    """Booking queryset."""

    def unchecked(self, base_date: date) -> Self:
        """Return bookings that weren't checked after its start date."""
        return self.filter(
            start__lte=base_date,
            status__in=[
                Booking.StatusChoices.CONFIRMED,
                Booking.StatusChoices.CHECKED_IN,
            ],
        )

    def pending(self) -> Self:
        """Filter by pending status."""
        return self.filter(status__in=[Booking.StatusChoices.PENDING])


class Booking(TimeStampedModel, models.Model):
    """Model definition for Booking."""

    class StatusChoices(models.TextChoices):
        """Booking status choices."""

        PENDING = "pending", _("Pending")
        CONFIRMED = "confirmed", _("Confirmed")
        CANCELED = "canceled", _("Canceled")
        CHECKED_IN = "checked_in", _("Checked in")
        CHECKED_OUT = "checked_out", _("Checked out")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(
        "hotels.Room", on_delete=models.CASCADE, related_name="bookings", editable=False
    )
    start = models.DateField()
    end = models.DateField()
    status = FSMField(choices=StatusChoices.choices, default=StatusChoices.PENDING)
    client = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    objects: ClassVar[models.Manager[Self]] = BookingQuerySet.as_manager()

    def __str__(self):
        """Return string representation."""
        return f"{self.room} - ({self.start} - {self.end})"

    def save(self, *args, **kwargs):
        """Save booking."""
        start = self.start
        end = self.end
        if start > end:
            raise ValueError("Start date cannot be greater than end date.")
        super().save(*args, **kwargs)

    @transition(
        field=status,
        source=StatusChoices.PENDING,
        target=StatusChoices.CONFIRMED,
    )
    def confirm(self):
        """Confirm booking."""

    @transition(
        field=status,
        source=[
            StatusChoices.PENDING,
            StatusChoices.CONFIRMED,
            StatusChoices.CHECKED_IN,
        ],
        target=StatusChoices.CANCELED,
    )
    def cancel(self):
        """Cancel booking."""
        self.room.check_out()

    @transition(
        field=status,
        source=StatusChoices.CONFIRMED,
        target=StatusChoices.CHECKED_IN,
    )
    def check_in(self):
        """Check in."""
        self.room.check_in()

    @transition(
        field=status,
        source=StatusChoices.CHECKED_IN,
        target=StatusChoices.CHECKED_OUT,
    )
    def check_out(self):
        """Check out."""
        self.room.check_out()
