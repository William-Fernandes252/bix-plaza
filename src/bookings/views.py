from rest_access_policy import AccessViewSetMixin
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import DetailSerializerMixin

from bookings import models, permissions, serializers


class BookingViewSet(AccessViewSetMixin, DetailSerializerMixin, ModelViewSet):
    """Book and manage reservations on hotel rooms."""

    queryset = models.Booking.objects.all()
    queryset_detail = models.Booking.objects.prefetch_related("room")
    serializer_class = serializers.BookingListSerializer
    serializer_detail_class = serializers.BookingDetailSerializer
    access_policy = permissions.BookingAccessPolicy
    filterset_fields = ["status", "start", "end"]

    @action(detail=True, methods=["post"])
    def check_in(self, request, *args, **kwargs) -> Response:
        booking: models.Booking = self.get_object()
        booking.check_in()
        return Response(self.get_serializer(booking).data, status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def check_out(self, request, *args, **kwargs) -> Response:
        booking: models.Booking = self.get_object()
        booking.check_out()
        return Response(self.get_serializer(booking).data, status.HTTP_200_OK)
