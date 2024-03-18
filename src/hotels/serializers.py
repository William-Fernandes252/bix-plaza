from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin

from addresses.models import Address
from addresses.serializers import AddressSerializer
from hotels import models
from users.serializers import AdminOnlyFieldsSerializerMixin


class RoomSerializer(PartialUpdateSerializerMixin, serializers.ModelSerializer):
    """Serializer for the Room class."""

    hotel = serializers.PrimaryKeyRelatedField(queryset=models.Hotel.objects.all())  # type: ignore
    url = serializers.HyperlinkedIdentityField("room-detail")

    class Meta:
        model = models.Room
        fields = (
            "id",
            "hotel",
            "number",
            "floor",
            "room_type",
            "created",
            "modified",
            "price",
            "url",
        )
        read_only_fields = ("id", "created", "modified")


class HotelListSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=False)
    url = serializers.HyperlinkedIdentityField("hotel-detail")
    rooms = RoomSerializer(many=True, write_only=True)
    manager = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=get_user_model().objects.all(),
        write_only=True,
    )
    owner = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=get_user_model().objects.all(),
        write_only=True,
    )

    class Meta:
        model = models.Hotel
        fields = [
            "id",
            "name",
            "address",
            "phone_number",
            "url",
            "rooms",
            "manager",
            "owner",
        ]
        read_only_fields = ["id"]


class HotelDetailSerializer(
    PartialUpdateSerializerMixin, AdminOnlyFieldsSerializerMixin, HotelListSerializer
):
    """Serializer for the Hotel class."""

    rooms = RoomSerializer(many=True, read_only=True)
    manager = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        required=False,
    )
    owner = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), required=False
    )

    class Meta(HotelListSerializer.Meta):
        fields = [
            "id",
            "name",
            "address",
            "phone_number",
            "created",
            "modified",
            "rooms",
            "manager",
            "owner",
            "url",
        ]
        read_only_fields = ["id", "created", "modified"]

    def update(self, instance: models.Hotel, validated_data):
        """Update the hotel instance."""
        address_data = validated_data.pop("address", None)
        if address_data:
            Address.objects.update_or_create(
                id=instance.address.id, defaults=address_data
            )

        instance = super().update(instance, validated_data)

        return instance
