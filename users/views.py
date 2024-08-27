import secrets

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from users.services import add_permission_user


class UserCreateView(CreateView):
    """Контроллер для регистрации пользователя"""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")  # после регистрации перенаправляем на вход#

    def form_valid(self, form):
        user = form.save()
        user.is_active = False  # регистрируем пользователя неактивным
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет! Перейди по ссылке {url} для подтверждения почты',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    """Функция для верификации email"""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    add_permission_user(user)
    return redirect(reverse('users:login'))


class ProfileView(LoginRequiredMixin, UpdateView):
    """Контроллер для просмотра профиля пользователя"""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка пользователей сервиса"""
    model = User

    def get_queryset(self, *args, **kwargs):
        """Метод выбирает список всех пользователей для менеджера и суперпользователя"""
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or user.has_perm('users.сan_block_user'):
            return queryset
        raise PermissionDenied


@login_required
@permission_required('users.сan_block_user')
def block_user(request, pk):
    user_item = get_object_or_404(User, pk=pk)
    if user_item.is_active:
        user_item.is_active = False
    else:
        user_item.is_active = True

    user_item.save()

    return redirect(reverse('users:list'))
