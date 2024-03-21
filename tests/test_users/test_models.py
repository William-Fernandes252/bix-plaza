import pytest

from users.models import User


@pytest.mark.django_db
class DescribeUser:
    class DescribeSave:
        def it_sets_default_groups(self, user: User):
            user.save()
            assert user.groups.exists()

    class DescribeGetAbsoluteUrl:
        def it_returns_url(self, user: User):
            assert user.get_absolute_url() == f"/users/{user.pk}/"

    class DescribeStr:
        def it_returns_email(self, user: User):
            assert str(user) == user.email

    class DescribeGetDefaultGroups:
        def it_returns_groups(self):
            groups = list(User.get_default_groups())
            assert len(groups) == 1
            assert groups[0].name == "clients"
