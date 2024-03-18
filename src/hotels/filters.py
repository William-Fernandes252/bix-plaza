from django_filters import rest_framework as filters

from hotels import models


class HotelFilter(filters.FilterSet):
    """Filter for the Hotel model."""

    city = filters.CharFilter(field_name="address__city", lookup_expr="icontains")
    uf = filters.CharFilter(field_name="address__uf", lookup_expr="iexact")

    class Meta:
        model = models.Hotel
        fields = {
            "name": ["exact", "icontains"],
        }


class RoomFilter(filters.FilterSet):
    """Filter for the Room model."""

    hotel = filters.NumberFilter(field_name="hotel__id")
    city = filters.CharFilter(
        field_name="hotel__address__city", lookup_expr="icontains"
    )
    uf = filters.CharFilter(field_name="hotel__address__uf", lookup_expr="iexact")

    class Meta:
        model = models.Room
        fields = {
            "room_type": ["exact"],
        }
