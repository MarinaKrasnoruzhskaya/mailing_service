from django.db import models


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
    """Класс для модели сообщения для рассылки"""
    theme = models.CharField(max_length=255, verbose_name='Тема письма', help_text='Введите тему письма')
    body = models.TextField(verbose_name='Тело письма', help_text='Введите тело письма')

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
