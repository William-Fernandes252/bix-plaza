import pytest
from django.contrib.auth.models import Group as AuthGroup

from users.management.commands.createdefaultgroups import Command
from users.models import Group


@pytest.mark.django_db
class TestCommand:
    def test_it_creates_all_default_groups(self):
        command = Command()
        command.handle()
        assert all(
            AuthGroup.objects.filter(name=group.value).exists() for group in Group
        )
