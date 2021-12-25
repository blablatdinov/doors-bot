from django.core.management.base import BaseCommand
from loguru import logger

from bot_init.views import tbot


class Command(BaseCommand):
    """Команда для запуска бота в режиме long polling."""

    help = 'command for start bot long polling mode'

    def handle(self, *args, **options):
        """Entrypoint."""
        logger.info('Start long polling...')
        tbot.infinity_polling()
