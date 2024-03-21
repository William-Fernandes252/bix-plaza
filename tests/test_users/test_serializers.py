import pytest
from django.test import RequestFactory
from django.utils import timezone
from rest_framework import serializers

from users.models import User
from users.serializers import (
    AdminOnlyFieldsSerializerMixin,
    UserSerializer,
    UserTokenObtainPairSerializer,
)


class ItemSerializer(AdminOnlyFieldsSerializerMixin, serializers.Serializer):
    """Serializer for testing."""

    slug = serializers.CharField(read_only=True, max_length=255)
    created = serializers.DateTimeField(read_only=True, default=lambda: timezone.now())
    modified = serializers.DateTimeField(read_only=True, default=lambda: timezone.now())

    class Meta:
        admin_only = ["created"]


@pytest.mark.django_db
class DescribeAdminOnlyFieldsSerializerMixin:
    """Test admin only fields serializer mixin."""

    def it_leaves_protected_fields_available_for_admin(
        self, admin: User, rf: RequestFactory
    ):
        """Remove admin only fields."""
        request = rf.get("/")
        request.user = admin
        serializer = ItemSerializer(context={"request": request})
        assert "created" in serializer.fields

    def it_removes_non_admin_only_fields(self, user: User, rf: RequestFactory):
        """Remove non admin only fields."""
        request = rf.get("/")
        request.user = user
        serializer = ItemSerializer(context={"request": request})
        assert "created" not in serializer.fields


@pytest.mark.django_db
class DescribeUserSerializer:
    class DescribeSerialize:
        def it_serializes_groups(self, user: User):
            serializer = UserSerializer(user)
            assert "groups" in serializer.data
            assert isinstance(serializer.data["groups"], list)
            assert len(serializer.data["groups"]) == 1
            assert serializer.data["groups"][0] == "clients"

        def it_serializes_admin_only_fields_for_admins(
            self, admin: User, rf: RequestFactory
        ):
            request = rf.get("/")
            request.user = admin
            serializer = UserSerializer(admin, context={"request": request})
            assert "is_staff" in serializer.data and "is_superuser" in serializer.data

        def it_does_not_serialize_admin_only_fields_for_non_admins(
            self, user: User, rf: RequestFactory
        ):
            request = rf.get("/")
            request.user = user
            serializer = UserSerializer(user, context={"request": request})
            assert all(
                field not in serializer.data for field in UserSerializer.Meta.admin_only
            )

    class DescribeDeserialize:
        def it_deserializes_groups(self):
            serializer = UserSerializer(
                data={
                    "groups": ["clients"],
                    "email": "william.fernandes@bix.com",
                    "name": "William Fernandes",
                    "phone_number": "1234567890",
                }
            )
            assert serializer.is_valid()
            user: User = serializer.save()
            assert user.groups.exists()
            group = user.groups.first()
            assert group and group.name == "clients"


@pytest.mark.django_db
class DescribeUserTokenObtainPairSerializer:
    class DescribeGetToken:
        def it_returns_a_token(self, user: User):
            serializer = UserTokenObtainPairSerializer(user)
            token = serializer.get_token(user)
            assert token

        def it_includes_the_correct_claims(self, user: User):
            serializer = UserTokenObtainPairSerializer(user)
            token = serializer.get_token(user)
            assert token["email"] == user.email
            assert token["name"] == user.name
            assert token["phone_number"] == user.phone_number
