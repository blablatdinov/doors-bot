from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Order(models.Model):
    """Создание модели для заказов на двери."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.TextField()
    info_from_measurer = models.TextField(null=True)
    deliveryman_datetime = models.DateTimeField(null=True)
    installer_datetime = models.DateTimeField(null=True)
