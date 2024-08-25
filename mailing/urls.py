from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    MailingSettingsListView, MailingSettingsDetailView, MailingSettingsCreateView, MailingSettingsUpdateView, \
    MailingSettingsDeleteView, MailingAttemptListView, disable_mailing_settings

app_name = MailingConfig.name

urlpatterns = [
    path('clients/', ClientListView.as_view(), name='clients'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='view_client'),
    path('client/create/', ClientCreateView.as_view(), name='create_client'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='update_client'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='delete_client'),
    path('messages/', MessageListView.as_view(), name='messages'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='view_message'),
    path('message/create/', MessageCreateView.as_view(), name='create_message'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='update_message'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='delete_message'),
    path('', MailingSettingsListView.as_view(), name='settings'),
    path('setting/<int:pk>/', MailingSettingsDetailView.as_view(), name='view_setting'),
    path('setting/create/',  MailingSettingsCreateView.as_view(), name='create_setting'),
    path('setting/<int:pk>/update/',  MailingSettingsUpdateView.as_view(), name='update_setting'),
    path('setting/<int:pk>/delete/', MailingSettingsDeleteView.as_view(), name='delete_setting'),
    path('block/<int:pk>/', disable_mailing_settings, name='disable_mailing'),
    path('attempts/', MailingAttemptListView.as_view(), name='attempts'),
]
