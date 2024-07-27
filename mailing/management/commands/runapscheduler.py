import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore


from mailing.services import change_mailing_status, send_mailing


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Кастомная команда для запуска автоматических попыток рассылки"""
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            change_mailing_status,
            trigger=CronTrigger(second="*/59"),  # Every 60 seconds
            id="change_mailing_status",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'change_mailing_status'.")

        scheduler.add_job(
            send_mailing,
            trigger=CronTrigger(second="*/59"),
            id="send_mailing",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added job: 'send_mailing'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")