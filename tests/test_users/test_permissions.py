import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from pytest_mock import MockerFixture
from rest_framework.request import Request

from tests.test_users.factories import UserFactory
from users.models import User
from users.permissions import UserAccessPolicy
from users.views import UserViewSet


class DescribeUserAccessPolicy:
    class DescribeIsSelf:
        def it_returns_true_for_self(self, user: User, mocker: MockerFixture):
            """Return True for self."""
            policy = UserAccessPolicy()
            request = mocker.MagicMock(Request, user=user)
            view = UserViewSet()
            view.setup(request)
            view.kwargs = {"pk": user.pk}
            assert policy.is_self(request, view)

        @pytest.mark.django_db
        def it_returns_false_for_other_user(
            self, user: User, mocker: MockerFixture, faker
        ):
            """Return False for other user."""
            other: User = UserFactory.create(email=faker.email())
            policy = UserAccessPolicy()
            request = mocker.MagicMock(Request, user=other)
            view = UserViewSet()
            view.setup(request)
            view.kwargs = {"pk": user.pk}
            assert not policy.is_self(request, view)

    class DescribeCreatePolicy:
        @pytest.fixture
        def view(self) -> UserViewSet:
            """Create a user view."""
            return UserViewSet(action="create")

        def it_returns_true_for_create_by_admin(
            self, admin: User, view: UserViewSet, rf: RequestFactory
        ):
            """Return True for admin."""
            policy = UserAccessPolicy()
            request = rf.post("/")
            request.user = admin
            assert policy.has_permission(request, view)

        def it_returns_true_for_create_by_anonymous(
            self, view: UserViewSet, rf: RequestFactory
        ):
            """Return True for anonymous."""
            policy = UserAccessPolicy()
            request = rf.post("/")
            request.user = AnonymousUser()
            assert policy.has_permission(request, view)

        def it_returns_false_for_client(
            self, user: User, view: UserViewSet, rf: RequestFactory
        ):
            """Return False for client."""
            policy = UserAccessPolicy()
            request = rf.post("/")
            request.user = user
            assert not policy.has_permission(request, view)

    class DescribeListPolicy:
        @pytest.fixture
        def view(self) -> UserViewSet:
            """Create a user view."""
            return UserViewSet(action="list")

        def it_returns_true_for_list_by_admin(
            self, admin: User, view: UserViewSet, rf: RequestFactory
        ):
            """Return True for admin."""
            policy = UserAccessPolicy()
            request = rf.get("/")
            view.setup(request)
            request.user = admin
            assert policy.has_permission(view.request, view)

        def it_returns_false_for_list_by_other_users(
            self, user: User, view: UserViewSet, rf: RequestFactory
        ):
            """Return False for client."""
            policy = UserAccessPolicy()
            request = rf.get("/")
            request.user = user
            view.setup(request)
            assert not policy.has_permission(request, view)

    class DescribeDetailActionsPolicy:
        @pytest.fixture(
            params=["update", "partial_update", "destroy", "retrieve", "me"]
        )
        def view(self, request: pytest.FixtureRequest) -> UserViewSet:
            """Create a user view."""
            return UserViewSet(action=request.param)

        @pytest.fixture
        def api_request(self, mocker: MockerFixture) -> Request:
            request = mocker.MagicMock(Request)
            request.method = "GET"
            return request

        def it_returns_true_for_authenticated(
            self, user: User, view: UserViewSet, api_request: Request
        ):
            """Return True for authenticated."""
            policy = UserAccessPolicy()
            api_request.user = user
            view.setup(api_request)
            view.kwargs = {"pk": user.pk}
            assert policy.has_permission(api_request, view)

        def it_returns_false_for_anonymous(
            self, view: UserViewSet, api_request: Request
        ):
            """Return False for anonymous."""
            policy = UserAccessPolicy()
            api_request.user = AnonymousUser()
            view.setup(api_request)
            view.kwargs = {"pk": api_request.user.pk}
            assert not policy.has_permission(api_request, view)
