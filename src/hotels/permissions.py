from typing import override

from rest_access_policy import AccessPolicy
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from hotels import models


class HotelAccessPolicy(AccessPolicy):
    """Access policy for the Hotel model."""

    statements = [
        {
            "action": ["create"],
            "principal": ["authenticated"],
            "effect": "allow",
        },
        {
            "action": [
                "list",
                "retrieve",
            ],
            "principal": ["*"],
            "effect": "allow",
        },
        {
            "action": [
                "destroy",
            ],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["user_must_be:owner"],
        },
        {
            "action": [
                "update",
                "partial_update",
            ],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["is_owner_or_manager"],
        },
    ]

    def get_hotel(self, view: GenericViewSet, *args, **kwargs) -> models.Hotel:
        return view.get_object()

    def user_must_be(
        self,
        request: Request,
        view: GenericViewSet,
        *args,
        **kwargs,
    ) -> bool:
        hotel: models.Hotel = self.get_hotel(view, *args, **kwargs)
        return hotel.owner == request.user

    def is_owner_or_manager(
        self,
        request: Request,
        view: GenericViewSet,
        *args,
        **kwargs,
    ) -> bool:
        hotel: models.Hotel = self.get_hotel(view, *args, **kwargs)
        return request.user.is_superuser or (
            hotel.owner == request.user or request.user == hotel.manager
        )


class RoomAccessPolicy(HotelAccessPolicy):
    """Access policy for the Room model."""

    statements = [
        {
            "action": ["create"],
            "principal": ["admin", "is_owner_or_manager"],
            "effect": "allow",
        },
        {
            "action": [
                "list",
                "retrieve",
            ],
            "principal": ["*"],
            "effect": "allow",
        },
        {
            "action": [
                "destroy",
            ],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["user_must_be:owner"],
        },
        {
            "action": [
                "update",
                "partial_update",
            ],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["user_must_be:owner"],
        },
    ]

    @override
    def get_hotel(self, view: GenericViewSet, *args, **kwargs) -> models.Hotel:
        room: models.Room = view.get_object()
        return room.hotel
