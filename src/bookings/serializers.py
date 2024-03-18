from typing import override

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from bookings import models
from hotels.models import Room
from hotels.serializers import RoomSerializer


class BookingListSerializer(serializers.ModelSerializer):
    """Booking serializer."""

    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    url = serializers.HyperlinkedIdentityField("booking-detail")

    class Meta:
        """Meta class."""

        model = models.Booking
        fields = "__all__"
        read_only_fields = ["id", "status"]

    def validate_start(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError(_("Start date cannot be in the past."))
        return value

    @override
    def validate(self, attrs):
        super().validate(attrs)

        start = attrs["start"]
        end = attrs["end"]
        if start > end:
            raise serializers.ValidationError(
                _("Start date cannot be greater than end date.")
            )

        if not attrs["room"].check_availability(attrs["start"], attrs["end"]):
            raise serializers.ValidationError(
                _("The room is not available for the given period.")
            )

        return attrs


class BookingDetailSerializer(BookingListSerializer):
    """Booking detail serializer."""

    room = RoomSerializer()

    class Meta(BookingListSerializer.Meta):
        """Meta class."""

        model = models.Booking
        read_only_fields = ["id", "room", "start", "end", "status", "client"]
