# Generated by Django 4.2.9 on 2024-08-27 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='is_published',
            field=models.BooleanField(default=False, help_text='Опубликовать блог?', verbose_name='Опубликовано'),
        ),
    ]
