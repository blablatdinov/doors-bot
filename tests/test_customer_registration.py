import pytest
from django.contrib.auth import get_user_model

from bot_init.service import customer_registration

pytestmark = [pytest.mark.django_db]

User = get_user_model()


@pytest.fixture()
def user(mixer):
    return mixer.blend(User)


@pytest.fixture()
def order(mixer, user):
    return mixer.blend('orders.Order', user=user)


def test(order):
    customer_registration(order.pk, 567)

    order.refresh_from_db()

    assert order.user.chat_id == 567
