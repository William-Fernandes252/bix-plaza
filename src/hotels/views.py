from typing import Any, override

from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_access_policy import AccessViewSetMixin
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_extensions.mixins import DetailSerializerMixin

from hotels import filters, models, permissions, serializers


class HotelViewSet(AccessViewSetMixin, DetailSerializerMixin, viewsets.ModelViewSet):
    """ViewSet for the Hotel class."""

    queryset = models.Hotel.objects.all()
    queryset_detail = models.Hotel.objects.prefetch_related("rooms")
    serializer_class = serializers.HotelListSerializer
    serializer_detail_class = serializers.HotelDetailSerializer
    access_policy = permissions.HotelAccessPolicy
    filterset_class = filters.HotelFilter

    @transaction.atomic
    @override
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    @override
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)


class RoomViewSet(AccessViewSetMixin, viewsets.ModelViewSet):
    """ViewSet for the Room class."""

    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    access_policy = permissions.RoomAccessPolicy
    filterset_class = filters.RoomFilter
