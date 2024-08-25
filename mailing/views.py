from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm, MessageForm, MailingSettingsForm
from mailing.models import Client, Message, MailingSettings, MailingAttempt
from mailing.services import change_mailing_status


class ClientListView(LoginRequiredMixin, ListView):
    """Контроллер для вывода списка клиентов"""
    model = Client

    def get_queryset(self, *args, **kwargs):
        """Метод выбирает клиентов, созданных авторизованным пользователем"""
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user

        queryset = queryset.filter(owner=self.request.user)
        return queryset


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
    """Контроллер для вывода списка сообщений"""
    model = Message

    def get_queryset(self, *args, **kwargs):
        """Метод выбирает сообщения, созданные авторизованным пользователем"""
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(owner=self.request.user)
        return queryset


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
    """Контроллер для вывода списка рассылок"""
    model = MailingSettings

    def get_queryset(self, *args, **kwargs):
        """Метод выбирает все рассылки для менеджера и суперпользователя
        или рассылки, созданные авторизованным пользователем"""
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_authenticated:
            if not user.is_superuser and not user.has_perm('mailing.view_mailingsettings'):
                queryset = queryset.filter(owner=self.request.user)
            return queryset
        raise PermissionDenied


class MailingSettingsDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для просмотра рассылки"""
    model = MailingSettings

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser or user.has_perm('mailing.view_mailingsettings') or user.id == self.object.owner_id:
                context_data['attempts'] = MailingAttempt.objects.filter(mailing=self.object).order_by('-datetime_last_try')
                return context_data
        raise PermissionDenied


@login_required
@permission_required('mailing.сan_disable_mailings')
def disable_mailing_settings(request, pk):
    mailing_settings_item = get_object_or_404(MailingSettings, pk=pk)
    if mailing_settings_item.is_disabled:
        mailing_settings_item.is_disabled = False
    else:
        mailing_settings_item.is_disabled = True

    mailing_settings_item.save()

    return redirect(reverse('mailing:settings'))


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
