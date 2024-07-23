from django.contrib import admin

from mailing.models import Client, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'comments')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('theme', 'body')
