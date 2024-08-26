from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from mailing.models import Client, Message, MailingSettings


def add_permission_user(user):
    """Функция задаёт права доступа для зарегистрированного пользователя"""
    perms = ['view', 'add', 'delete', 'change']
    models = {'client': Client, 'message': Message, 'mailingsettings': MailingSettings}
    for name, model in models.items():
        content_type = ContentType.objects.get_for_model(model)
        for perm in perms:
            codename = f"{perm}_{name}"
            permission = Permission.objects.get(codename=codename, content_type=content_type,)
            user.user_permissions.add(permission)
