import smtplib
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail

from mailing.models import MailingSettings, MailingAttempt


def change_mailing_status():
    """Функция изменения статуса рассылок"""
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = MailingSettings.objects.exclude(mailing_status='completed').exclude(is_disabled=True)
    for mailing in mailings:
        if mailing.end_datetime < current_datetime:
            mailing.mailing_status = 'completed'
            mailing.save(update_fields=['mailing_status'])
        if mailing.mailing_status == 'created' and mailing.start_datetime <= current_datetime:
            mailing.mailing_status = 'launched'
            mailing.save(update_fields=['mailing_status'])


def is_next_send_time(mailing: MailingSettings, attempt: MailingAttempt, current: datetime) -> bool:
    """Функция проверки на следующее время рассылки"""
    time_difference = current - attempt.datetime_last_try if attempt else 0

    if attempt:
        if mailing.periodicity == 'once a day' and time_difference >= timedelta(days=1):
            return True
        elif mailing.periodicity == 'once a week' and time_difference >= timedelta(days=7):
            return True
        elif mailing.periodicity == 'once a month' and time_difference >= timedelta(days=30):
            return True
    else:  # рассылка запущена, но попыток рассылки еще не было
        return True

    return False


def send_mailing():
    """Функция отправки рассылок"""
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    # выбираем все запущенные рассылки
    mailings = MailingSettings.objects.filter(mailing_status='launched')

    for mailing in mailings:
        attempts = MailingAttempt.objects.filter(mailing=mailing)  # получаем все попытки рассылки для текущей рассылки
        end_attempt = attempts.order_by('-datetime_last_try')[0] if attempts else None  # получаем последнюю попытку

        if is_next_send_time(mailing, end_attempt, current_datetime):
            try:
                result = send_mail(
                    subject=mailing.message.theme,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in mailing.clients.all()],
                    fail_silently=False,
                )
                status = 'Successfully' if result else 'Not successful'
                response = ''
            except smtplib.SMTPException as e:
                status = 'Not successful'
                response = str(e)

            MailingAttempt.objects.create(
                attempt_status=status,
                response_mail_server=response,
                mailing=mailing,
                datetime_last_try=current_datetime,
            )
            print('Рассылка отправлена')


def start():
    """Функция старта периодических задач"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(change_mailing_status, 'interval', seconds=59)
    scheduler.add_job(send_mailing, 'interval', seconds=59)
    scheduler.start()
