from django.contrib.auth.models import Group
from rest_framework import serializers

from users import models


class AdminOnlyFieldsSerializerMixin:
    """Serializer mixin to remove fields if the user is not an admin.

    ```python

    # Usage:

    class MyActivityModelSerializer(
        AdminOnlyFieldsSerializerMixin,
        ActivitySerializer
    ):
        ...

    serializer = MyActivityModelSerializer(
        context={"request": request},
        admin_only=["user", "content_type"],
    )

    ```
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the serializer."""
        admin_only_fields = set(
            kwargs.pop(
                "admin_only",
                getattr(self.Meta, "admin_only", []),  # type: ignore
            )
        )
        super().__init__(*args, **kwargs)  # type: ignore

        context = kwargs.get("context")
        if not context:
            return

        request = context.get("request")
        if not request:
            return

        if request.user and not getattr(request.user, "is_superuser", False):
            for field_name in admin_only_fields:
                self.fields.pop(field_name)  # type: ignore[attr-defined]


class UserSerializer(AdminOnlyFieldsSerializerMixin, serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(  # type: ignore[var-annotated]
        slug_field="name", many=True, queryset=Group.objects.all(), read_only=False
    )

    class Meta:
        model = models.User
        fields = (
            "id",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "groups",
        )
        read_only_fields = ("id", "date_joined")
        extra_kwargs = {
            "password": {"write_only": True},
        }
        admin_only = ("is_superuser", "is_staff")

    def create(self, validated_data):
        group_names = validated_data.pop("groups", models.User.get_default_groups())
        groups = Group.objects.filter(name__in=group_names)
        user = models.User.objects.create_user(**validated_data)
        user.groups.set(groups)
        return user
