from django.conf import settings
from django.core.management.base import BaseCommand

from bot_init.service import update_webhook


class Command(BaseCommand):
    """Command for update webhook."""

    help = 'command for update webhook'

    def handle(self, *args, **options):
        """Entrypoint."""
        update_webhook(f'{settings.TG_BOT.webhook_host}/bot_init/{settings.TG_BOT.token}')
