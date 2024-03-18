from typing import Any, override

from django.db import transaction
from rest_access_policy import AccessViewSetMixin
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_extensions.mixins import DetailSerializerMixin

from hotels import filters, models, permissions, serializers


class HotelViewSet(AccessViewSetMixin, DetailSerializerMixin, viewsets.ModelViewSet):
    """ViewSet for the Hotel class."""

    queryset = models.Hotel.objects.all()
    serializer_class = serializers.HotelListSerializer
    serializer_detail_class = serializers.HotelDetailSerializer
    access_policy = permissions.HotelAccessPolicy
    filterset_class = filters.HotelFilter

    @transaction.atomic
    @override
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)


class RoomViewSet(AccessViewSetMixin, viewsets.ModelViewSet):
    """ViewSet for the Room class."""

    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    access_policy = permissions.RoomAccessPolicy
    filterset_class = filters.RoomFilter
