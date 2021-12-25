from django.conf import settings
from telebot import TeleBot


def get_tbot_instance() -> TeleBot:
    """Получаем экземпляр класса TeleBot для удобной работы с API."""
    return TeleBot(settings.TG_BOT.token)
