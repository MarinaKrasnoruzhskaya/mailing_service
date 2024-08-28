from time import sleep

from django.apps import AppConfig


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

# сделать активными это строки для автоматического запуска попыток рассылки
    # def ready(self):
    #     from mailing.services import start
    #     sleep(2)
    #     start()
