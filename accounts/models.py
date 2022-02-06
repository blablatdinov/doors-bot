from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Модель пользователя, пересоздана для удобного расширенияя."""

    father_name = models.CharField(_('Отчество'), max_length=64, null=True, blank=True)
    chat_id = models.BigIntegerField(_('Id в телеграм'), null=True)
    phone = models.CharField(_('Номер телефона'), max_length=16, null=True, blank=True)
