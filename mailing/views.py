from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from blog.models import BlogPost
from blog.services import get_blogpost_for_cache
from mailing.forms import ClientForm, MessageForm, MailingSettingsForm
from mailing.models import Client, Message, MailingSettings, MailingAttempt
from mailing.services import get_statistic_mailing_for_cache


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Контроллер для вывода списка клиентов"""
    model = Client
    permission_required = 'mailing.view_client'

    def get_queryset(self, *args, **kwargs):
        """Метод выбирает клиентов, созданных авторизованным пользователем"""
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_authenticated:
            if not user.is_superuser or not user.has_perm('mailing.view_client'):
                queryset = queryset.filter(owner=self.request.user)
            return queryset
        raise PermissionDenied


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Контроллер для вывода детальной информации о клиенте"""
    model = Client
    permission_required = 'mailing.view_client'


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер для создания клиента"""
    model = Client
    form_class = ClientForm
    permission_required = 'mailing.add_client'
    success_url = reverse_lazy('mailing:clients')

    def form_valid(self, form, **kwargs):
        """Метод для автоматической привязки владельца клиента - пользователя"""
        client = form.save()
        client.owner = self.request.user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер для редактирования клиента"""
    model = Client
    form_class = ClientForm
    permission_required = 'mailing.change_client'

    def get_success_url(self):
        return reverse('mailing:view_client', args=[self.kwargs.get('pk')])


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер для удаления клиента"""
    model = Client
    permission_required = 'mailing.delete_client'
    success_url = reverse_lazy('mailing:clients')


class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Контроллер для вывода списка сообщений"""
    model = Message
    permission_required = 'mailing.view_message'

    def get_queryset(self, *args, **kwargs):
        """Метод выбирает сообщения, созданные авторизованным пользователем или все сообщения для суперюзера"""
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_authenticated:
            if not user.is_superuser or not user.has_perm('mailing.view_message'):
                queryset = queryset.filter(owner=self.request.user)
            return queryset
        raise PermissionDenied


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Контроллер для вывода детальной информации о сообщении"""
    model = Message
    permission_required = 'mailing.view_message'


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер для создания сообщения"""
    model = Message
    form_class = MessageForm
    permission_required = 'mailing.add_message'
    success_url = reverse_lazy('mailing:messages')

    def form_valid(self, form, **kwargs):
        """Метод для автоматической привязки владельца сообщения - пользователя"""
        message = form.save()
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер для редактирования сообщения"""
    model = Message
    form_class = MessageForm
    permission_required = 'mailing.change_message'

    def get_success_url(self):
        return reverse('mailing:view_message', args=[self.kwargs.get('pk')])


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер для удаления сообщения"""
    model = Message
    permission_required = 'mailing.delete_message'
    success_url = reverse_lazy('mailing:messages')


class MailingSettingsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Контроллер для вывода списка рассылок"""
    model = MailingSettings
    permission_required = 'mailing.view_mailingsettings'

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


class MailingSettingsDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Контроллер для просмотра рассылки"""
    model = MailingSettings
    permission_required = 'mailing.view_mailingsettings'

    def get_context_data(self, **kwargs):
        """Метод выбирает попытки рассылок для данной рассылки"""
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser or user.has_perm('mailing.view_mailingsettings') or user.id == self.object.owner_id:
                context_data['attempts'] = MailingAttempt.objects.filter(mailing=self.object).order_by(
                    '-datetime_last_try')
                return context_data
        raise PermissionDenied


@login_required
@permission_required('mailing.сan_disable_mailings')
def disable_mailing_settings(request, pk):
    """Контроллер для отключения рассылки"""
    mailing_settings_item = get_object_or_404(MailingSettings, pk=pk)
    if mailing_settings_item.is_disabled:
        mailing_settings_item.is_disabled = False
    else:
        mailing_settings_item.is_disabled = True

    mailing_settings_item.save()

    return redirect(reverse('mailing:settings'))


class MailingSettingsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер для создания рассылки"""
    model = MailingSettings
    form_class = MailingSettingsForm
    permission_required = 'mailing.add_mailingsettings'
    success_url = reverse_lazy('mailing:settings')

    def get_form(self, form_class=None):
        """Метод возвращает в форме клиентов и сообщения, созданные авторизованным пользователем"""
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['message'].queryset = Message.objects.filter(owner=self.request.user)
        form.fields['clients'].queryset = Client.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form, **kwargs):
        """Метод для автоматической привязки владельца рассылки - пользователя"""
        mailing = form.save()
        mailing.owner = self.request.user
        mailing.save()
        return super().form_valid(form)


class MailingSettingsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер для редактирования рассылки"""
    model = MailingSettings
    form_class = MailingSettingsForm
    permission_required = 'mailing.change_mailingsettings'

    def get_success_url(self):
        return reverse('mailing:view_setting', args=[self.kwargs.get('pk')])

    def get_form(self, form_class=None):
        """Метод возвращает в форме клиентов и сообщения, созданные авторизованным пользователем"""
        form = super().get_form(form_class)
        form.fields['message'].queryset = Message.objects.filter(owner=self.request.user)
        form.fields['clients'].queryset = Client.objects.filter(owner=self.request.user)
        return form


class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления рассылки"""
    model = MailingSettings
    permission_required = 'mailing.delete_mailingsettings'
    success_url = reverse_lazy('mailing:settings')


class MailingAttemptListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Контроллер для вывода списка попыток рассылок"""
    model = MailingAttempt
    permission_required = 'mailing.view_mailingattempt'

    def get_context_data(self, *args, **kwargs):
        """Метод выбирает все попытки рассылок для суперпользователя
        или попытки рассылок, созданные авторизованным пользователем"""
        context_data = super().get_context_data(*args, **kwargs)
        user = self.request.user
        if user.is_authenticated:
            if not user.is_superuser and user.has_perm('mailing.view_mailingattempt'):
                mailings = MailingSettings.objects.filter(owner_id=user.id)
                attempts = []
                for mailing in mailings:
                    attemps_mailing = self.object_list.filter(mailing_id=mailing.id)
                    attempts.extend(attemps_mailing)
                context_data['object_list'] = attempts
            return context_data
        raise PermissionDenied


class IndexView(TemplateView):
    """Контроллер для главной страницы"""
    template_name = "mailing/index.html"

    def get_context_data(self, **kwargs):
        """Метод передает кол-во всего рассылок, активных рассылок, уникальных клиентов и 3 случайных статьи из блога"""
        context = super().get_context_data(**kwargs)
        context['mailing_count'] = get_statistic_mailing_for_cache()['mailing_count']
        context['active_mailing_count'] = get_statistic_mailing_for_cache()['active_mailing_count']
        context['unique_clients_count'] = get_statistic_mailing_for_cache()['unique_clients_count']
        context["blog_list"] = get_blogpost_for_cache().order_by('?')[:3]
        return context
