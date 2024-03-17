from rest_access_policy import AccessViewSetMixin
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.permissions import UserAccessPolicy
from users.serializers import UserSerializer


class UserViewSet(AccessViewSetMixin, ModelViewSet):
    """ViewSet for the User class."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    access_policy = UserAccessPolicy
