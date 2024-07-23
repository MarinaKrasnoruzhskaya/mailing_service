from django.db import models
from django.utils import timezone


class Client(models.Model):
    """Класс для модели клиента - тех, кто получает рассылки"""
    email = models.EmailField(verbose_name='Email', help_text='Введите email', unique=True)
    name = models.CharField(max_length=150, verbose_name='Ф.И.О.', help_text='Введите Ф.И.О.')
    comments = models.TextField(verbose_name='Комментарий', help_text='Введите комментарий', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    """Класс для модели сообщение для рассылки"""
    theme = models.CharField(max_length=255, verbose_name='Тема письма', help_text='Введите тему письма')
    body = models.TextField(verbose_name='Тело письма', help_text='Введите тело письма')

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingSettings(models.Model):
    """Класс для модели настройка рассылки"""
    PERIODS = (
        ('once a day', 'раз в день'),
        ('once a week', 'раз в неделю'),
        ('once a month', 'раз в месяц'),
    )
    STATUSES = (
        ('created', 'создана'),
        ('launched', 'запущена'),
        ('completed', 'завершена'),
    )

    start_datetime = models.DateTimeField(
        verbose_name='Дата и время первой отправки рассылки',
        help_text='Введите дату и время первой отправки рассылки',
    )
    end_datetime = models.DateTimeField(
        verbose_name='Дата и время окончания рассылки',
        help_text='Введите дату и время окончания рассылки',
    )
    periodicity = models.CharField(
        verbose_name='Периодичность рассылки',
        help_text='Выберите периодичность рассылки',
        choices=PERIODS,
        default='раз в день',
    )
    mailing_status = models.CharField(
        verbose_name='Статус рассылки',
        help_text='Выберите статус рассылки',
        choices=STATUSES,
        default='создана',
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name='Сообщение',
        help_text='Выберите сообщение для рассылки',
    )
    clients = models.ManyToManyField(
        Client,
        related_name='client_of',
        verbose_name='Клиенты для рассылки',
        help_text='Выберите клиентов для рассылки',
    )

    def __str__(self):
        return f"Рассылка {self.pk}: с {self.start_datetime} с периодичностью {self.periodicity}"

    class Meta:
        verbose_name = 'Настройки рассылки'
        verbose_name_plural = 'Настройки рассылок'
