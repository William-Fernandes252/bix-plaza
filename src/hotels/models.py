import uuid
from datetime import date
from typing import override

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from bookings.models import Booking
from hotels.querysets import RoomQuerySet
from users.models import Group


class Hotel(TimeStampedModel, models.Model):
    """Model definition for Hotel."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(_("Hotel email"), max_length=254)
    address = models.ForeignKey("addresses.Address", on_delete=models.CASCADE)
    manager = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="hotel"
    )
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="hotels"
    )
    phone_number = PhoneNumberField()

    class Meta:
        """Meta definition for Hotel."""

        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"

    def __str__(self):
        """Unicode representation of Hotel."""
        return f"{self.name} ({self.address})"

    @override
    def save(self, *args, **kwargs):
        """Persist the hotel instance.

        Raises
        ------
            ValidationError: If the manager is not in the manager group.

        """
        if not self.manager.groups.filter(name=Group.MANAGERS.value).exists():
            raise ValidationError(_("The hotel manager must be in the manager group."))
        super().save(*args, **kwargs)

    @override
    def get_absolute_url(self):
        return reverse("hotel-detail", kwargs={"pk": self.pk})


class Room(TimeStampedModel, models.Model):  # type: ignore[django-manager-missing]
    """Model definition for Room."""

    class RoomType(models.TextChoices):
        """Enum for room types."""

        SINGLE = "single", _("Single")
        DOUBLE = "double", _("Double")
        TRIPLE = "triple", _("Triple")
        QUADRUPLE = "quadruple", _("Quadruple")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hotel = models.ForeignKey(
        "hotels.Hotel", on_delete=models.CASCADE, related_name="rooms"
    )
    number = models.PositiveSmallIntegerField()
    floor = models.PositiveSmallIntegerField()
    room_type = models.CharField(max_length=9, choices=RoomType.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    occupied = models.BooleanField(default=False)

    objects = RoomQuerySet.as_manager()

    class Meta:
        """Meta definition for Room."""

        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self):
        """Unicode representation of Room."""
        return f"{self.number} - {self.hotel} - {self.room_type}"

    @override
    def get_absolute_url(self):
        return reverse("room-detail", kwargs={"pk": self.pk})

    def check_availability(self, start: date, end: date) -> bool:
        """Check if the room is available in the given period."""
        return not self.bookings.filter(
            (
                models.Q(start__lte=start, end__gte=start)
                | models.Q(start__lte=end, end__gte=end)
            )
            & models.Q(
                status__in=[
                    Booking.StatusChoices.CONFIRMED,
                    Booking.StatusChoices.CHECKED_IN,
                ]
            )
        ).exists()

    def check_in(self):
        """Check in the room."""
        self.occupied = True
        self.save()

    def check_out(self):
        """Check out the room."""
        self.occupied = False
        self.save()
