import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

pytestmark = [pytest.mark.django_db]

User = get_user_model()


@pytest.fixture()
def user(mixer):
    return mixer.blend(User)


@pytest.fixture()
def user_without_groups(mixer):
    return mixer.blend(User)


@pytest.fixture(autouse=True)
def group(mixer, user):
    g = mixer.blend(Group, name='manager')
    user.groups.add(g)
    user.save()


def test(user):
    assert user.role() == 'manager'


def test_user_without_group(user_without_groups):
    assert user_without_groups.role() is None
