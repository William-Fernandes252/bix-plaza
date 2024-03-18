from typing import override

from django.db.models.query import QuerySet
from rest_access_policy import AccessPolicy
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from bookings import models
from users.managers import UserManager


class BookingAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create"],
            "principal": ["authenticated"],
            "effect": "allow",
        },
        {
            "action": ["list", "retrieve"],
            "principal": ["admin", "managers", "clients"],
            "effect": "allow",
        },
        {
            "action": [
                "update",
                "partial_update",
                "destroy",
                "confirm",
                "cancel",
                "check_in",
                "check_out",
            ],
            "principal": ["admin", "managers", "clients"],
            "effect": "allow",
            "condition": ["is_owner_or_manager"],
        },
    ]

    def is_owner_or_manager(
        self, request: Request, view: GenericViewSet, *args, **kwargs
    ):
        """Validate if the user is the owner of the booking."""
        booking: models.Booking = view.get_object()
        return booking.client == request.user or UserManager.is_manager(request.user)

    @override
    @classmethod
    def scope_queryset(cls, request: Request, queryset: QuerySet):
        if request.user.is_superuser:
            return queryset
        if UserManager.is_manager(request.user):
            return queryset.filter(room__hotel__manager=request.user)
        return queryset.filter(client=request.user)
