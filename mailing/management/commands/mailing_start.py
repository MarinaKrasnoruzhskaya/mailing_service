from django.core.management import BaseCommand

from mailing.services import send_mailing, change_mailing_status


class Command(BaseCommand):
    def handle(self, *args, **options):
        change_mailing_status()
        send_mailing()
