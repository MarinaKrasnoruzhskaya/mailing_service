from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from mailing.models import Client, Message, MailingSettings, MailingAttempt


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('mailing:clients')


class ClientUpdateView(UpdateView):
    model = Client
    fields = '__all__'

    def get_success_url(self):
        return reverse('mailing:view_client', args=[self.kwargs.get('pk')])


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('mailing:messages')


class MessageUpdateView(UpdateView):
    model = Message
    fields = '__all__'

    def get_success_url(self):
        return reverse('mailing:view_message', args=[self.kwargs.get('pk')])


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages')


class MailingSettingsListView(ListView):
    model = MailingSettings


class MailingSettingsDetailView(DetailView):
    model = MailingSettings

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['attempts'] = MailingAttempt.objects.filter(mailing=self.object).order_by('-datetime_last_try')
        return context_data


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    fields = '__all__'
    success_url = reverse_lazy('mailing:settings')


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    fields = '__all__'

    def get_success_url(self):
        return reverse('mailing:view_setting', args=[self.kwargs.get('pk')])


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:settings')


class MailingAttemptListView(ListView):
    model = MailingAttempt
