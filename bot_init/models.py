from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    info = models.TextField()
    info_from_measurer = models.TextField()
    deliveryman_datetime = models.DateTimeField(default=timezone.now)
    installer_datetime = models.DateTimeField(default=timezone.now)