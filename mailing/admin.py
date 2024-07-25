from django.contrib import admin

from mailing.models import Client, Message, MailingSettings, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'comments')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('theme', 'body')


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('start_datetime', 'end_datetime', 'periodicity', 'mailing_status', 'message')


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('datetime_last_try', 'attempt_status', 'response_mail_server', 'mailing')
    list_filter = ('mailing',)
