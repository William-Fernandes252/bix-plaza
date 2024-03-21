import pytest
from django.core.management import call_command

from tests.test_users.factories import User, UserFactory


@pytest.fixture()
def django_db_setup(django_db_setup, django_db_blocker):
    """Django database setup fixture.

    This extends the default behavior by adding the creation of default groups
    """
    with django_db_blocker.unblock():
        call_command("createdefaultgroups")


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    """Set the faker locales."""
    return ["en_US", "pt_BR"]


@pytest.fixture(scope="session", autouse=True)
def faker_seed():
    """Set the faker seed."""
    return 12345


@pytest.fixture
def user(db, faker) -> User:
    """Create a user for testing."""
    return UserFactory.create(email=faker.email())


@pytest.fixture
def admin(user: User) -> User:
    """Create a test user."""
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return user
