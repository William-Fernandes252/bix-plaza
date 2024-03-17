from rest_access_policy import AccessViewSetMixin
from rest_framework.viewsets import ModelViewSet

from addresses.filters import AddressFilter
from addresses.models import Address
from addresses.permissions import AddressAccessPolicy
from addresses.serializers import AddressSerializer


class AddressViewSet(AccessViewSetMixin, ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    access_policy = AddressAccessPolicy
    filterset_class = AddressFilter
    ordering_fields = "__all__"
