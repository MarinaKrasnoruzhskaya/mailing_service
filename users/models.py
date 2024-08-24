from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Класс для пользователя"""
    username = None
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Введите email')
    phone_number = PhoneNumberField(
        verbose_name='Номер телефона',
        help_text='Введите номер телефона',
        **NULLABLE
    )
    company = models.CharField(
        max_length=200,
        verbose_name='Название компании',
        help_text='Введите название компании',
        **NULLABLE
    )

    token = models.CharField(max_length=100, verbose_name='Token', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
