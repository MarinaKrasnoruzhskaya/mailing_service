from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView

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
]
