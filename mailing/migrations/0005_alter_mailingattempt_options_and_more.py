# Generated by Django 5.0.7 on 2024-07-26 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0004_mailingattempt'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailingattempt',
            options={'ordering': ['-id'], 'verbose_name': 'Попытка рассылки', 'verbose_name_plural': 'Попытки рассылок'},
        ),
        migrations.AlterModelOptions(
            name='mailingsettings',
            options={'ordering': ['-id'], 'verbose_name': 'Настройки рассылки', 'verbose_name_plural': 'Настройки рассылок'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-id'], 'verbose_name': 'Сообщение', 'verbose_name_plural': 'Сообщения'},
        ),
    ]
