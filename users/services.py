from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from blog.models import BlogPost
from mailing.models import Client, Message, MailingSettings, MailingAttempt


def add_permission_user(user):
    """Функция задаёт права доступа для зарегистрированного пользователя"""
    perms = ['view', 'add', 'delete', 'change']
    models = [
        {'name': 'client', 'model': Client, 'permissions': perms},
        {'name': 'message', 'model': Message, 'permissions': perms},
        {'name': 'mailingsettings', 'model': MailingSettings, 'permissions': perms},
        {'name': 'mailingattempt', 'model': MailingAttempt, 'permissions': ['view',]},
        {'name': 'blogpost', 'model': BlogPost, 'permissions': ['view', 'add',]},
    ]
    for model in models:
        content_type = ContentType.objects.get_for_model(model['model'])
        for perm in model['permissions']:
            codename = f"{perm}_{model['name']}"
            permission = Permission.objects.get(codename=codename, content_type=content_type,)
            user.user_permissions.add(permission)
