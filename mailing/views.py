from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm, MessageForm, MailingSettingsForm
from mailing.models import Client, Message, MailingSettings, MailingAttempt


class ClientListView(LoginRequiredMixin, ListView):
    model = Client


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')

    def form_valid(self, form, **kwargs):
        """Метод для автоматической привязки владельца клиента - пользователя"""
        client = form.save()
        client.owner = self.request.user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing:view_client', args=[self.kwargs.get('pk')])


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')

    def form_valid(self, form, **kwargs):
        """Метод для автоматической привязки владельца сообщения - пользователя"""
        message = form.save()
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('mailing:view_message', args=[self.kwargs.get('pk')])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages')


class MailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings


class MailingSettingsDetailView(LoginRequiredMixin, DetailView):
    model = MailingSettings

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['attempts'] = MailingAttempt.objects.filter(mailing=self.object).order_by('-datetime_last_try')
        return context_data


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:settings')

    def form_valid(self, form, **kwargs):
        """Метод для автоматической привязки владельца рассылки - пользователя"""
        mailing = form.save()
        mailing.owner = self.request.user
        mailing.save()
        return super().form_valid(form)


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm

    def get_success_url(self):
        return reverse('mailing:view_setting', args=[self.kwargs.get('pk')])


class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:settings')


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
