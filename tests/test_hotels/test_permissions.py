import pytest
from pytest_mock import MockerFixture
from rest_framework.request import Request

from hotels import models, permissions, views
from users.models import User


class DescribeHotelAccessPolicy:
    class DescribeReadPolicy:
        @pytest.fixture(params=["list", "retrieve"])
        def view(self, request: pytest.FixtureRequest) -> views.HotelViewSet:
            """Create a user view."""
            return views.HotelViewSet(action=request.param)

        @pytest.fixture
        def api_request(self, mocker: MockerFixture) -> Request:
            request = mocker.MagicMock(Request)
            request.method = "GET"
            return request

        def it_returns_true_for_authenticated(
            self, user: User, view: views.HotelViewSet, api_request: Request
        ):
            """Return True for authenticated."""
            policy = permissions.HotelAccessPolicy()
            api_request.user = user
            assert policy.has_permission(api_request, view)

    class DescribeCreatePolicy:
        @pytest.fixture
        def view(self) -> views.HotelViewSet:
            """Create a user view."""
            return views.HotelViewSet(action="create")

        @pytest.fixture
        def api_request(self, mocker: MockerFixture) -> Request:
            request = mocker.MagicMock(Request)
            request.method = "POST"
            return request

        def it_returns_true_for_authenticated(
            self, user: User, view: views.HotelViewSet, api_request: Request
        ):
            """Return True for authenticated."""
            policy = permissions.HotelAccessPolicy()
            api_request.user = user
            assert policy.has_permission(api_request, view)

    @pytest.mark.skip
    class DescribeDestroyPolicy:
        @pytest.fixture
        def api_request(self, mocker: MockerFixture) -> Request:
            request: Request = mocker.MagicMock(Request)
            request.method = "DELETE"
            return request

        @pytest.fixture
        def view(self) -> views.HotelViewSet:
            """Create a user view."""
            view = views.HotelViewSet(action="destroy")
            return view

        def it_returns_true_for_owner(
            self,
            view: views.HotelViewSet,
            api_request: Request,
            hotel: models.Hotel,
        ):
            """Return True for authenticated."""
            policy = permissions.HotelAccessPolicy()
            api_request.user = hotel.owner
            view.setup(api_request, pk=hotel.pk)
            assert policy.has_permission(api_request, view)

        def it_returns_false_for_non_owner(
            self,
            user: User,
            view: views.HotelViewSet,
            api_request: Request,
            hotel: models.Hotel,
        ):
            """Return False for authenticated."""
            policy = permissions.HotelAccessPolicy()
            api_request.user = user
            view.setup(api_request, pk=hotel.pk)
            assert not policy.has_permission(api_request, view)
