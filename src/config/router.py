from django.conf import settings
from rest_framework import routers

from addresses.views import AddressViewSet
from users.views import UserViewSet

router = routers.DefaultRouter() if settings.DEBUG else routers.SimpleRouter()

router.register("users", UserViewSet)
router.register("addresses", AddressViewSet)
