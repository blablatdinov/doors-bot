import pytest
from django.test.client import Client

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def client():
    return Client()


@pytest.fixture()
def mixer():
    from mixer.backend.django import mixer
    return mixer
