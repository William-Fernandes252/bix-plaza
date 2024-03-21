import pytest

from users.managers import UserManager
from users.models import User


@pytest.mark.django_db
class DescribeUserManager:
    @pytest.fixture
    def manager(self) -> UserManager:
        """Create a user manager with the User model."""
        manager = UserManager()
        manager.model = User
        return manager

    def it_creates_user(self, manager: UserManager):
        """Create a user."""
        user = manager.create_user(email="william.fernandes@bix.com", password="123456")
        assert user

    def it_creates_superuser(self, manager: UserManager):
        """Create a superuser."""
        user = manager.create_superuser(
            email="william.fernandes@bix.com", password="123456"
        )
        assert all([user.is_superuser, user.is_staff])
