import smtplib
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.core.mail import send_mail

from mailing.models import MailingSettings, MailingAttempt


def is_next_send_time(mailing: MailingSettings, attempt: MailingAttempt, current: datetime) -> bool:
    """Функция проверки на следующее время рассылки"""
    time_difference = current - attempt.datetime_last_try if attempt else 0
    print(f'Time difference: {time_difference}')
    if mailing.mailing_status == 'created' and mailing.start_datetime <= current <= mailing.end_datetime:
        return True
    elif mailing.periodicity == 'once a day' and time_difference >= timedelta(days=1):
        return True
    elif mailing.periodicity == 'once a week' and time_difference >= timedelta(days=7):
        return True
    elif mailing.periodicity == 'once a month' and time_difference >= timedelta(days=30):
        return True
    return False


def send_mailing():
    """Функция отправки рассылок"""
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    # выбираем все созданные или запущенные рассылки
    mailings = MailingSettings.objects.filter(start_datetime__lte=current_datetime).filter(
        mailing_status__in=['created', 'launched']
    )

    for mailing in mailings:
        attempts = MailingAttempt.objects.filter(mailing=mailing)  # получаем все попытки рассылки для текущей рассылки
        end_attempt = attempts.order_by('-datetime_last_try')[0] if attempts else None  # получаем последнюю попытку рассылки

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

            if mailing.mailing_status == 'created':
                mailing.mailing_status = 'launched'
                mailing.save(update_fields=['mailing_status'])

        if mailing.end_datetime <= current_datetime:
            mailing.mailing_status = 'completed'
            mailing.save(update_fields=['mailing_status'])
