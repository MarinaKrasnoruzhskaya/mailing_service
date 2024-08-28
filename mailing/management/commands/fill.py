import json

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.db import connection

from blog.models import BlogPost
from mailing.models import Client, Message, MailingSettings, MailingAttempt
from users.models import User


class Command(BaseCommand):
    """Класс для кастомной команды заполнения БД"""

    @staticmethod
    def json_read(name_file: str) -> dict:
        """Метод считывает данные из json-файла"""
        with open(name_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    @staticmethod
    def json_read_data(name_file, name_app, name_model):
        """Метод читает данные из json-файла по конкретному приложению и модели"""
        data = []

        for item in Command.json_read(name_file):
            if item["model"] == f"{name_app}.{name_model}":
                data.append(item)

        return data

    @staticmethod
    def truncate_table_restart_id(name_app, name_model):
        """Метод очищает таблицу и обнуляет id=1"""
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {name_app}_{name_model} RESTART IDENTITY CASCADE')

    @staticmethod
    def select_setval_id(name_app, name_model):
        """Метод устанавливает последний id в таблице"""
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT SETVAL('{name_app}_{name_model}_id_seq', (SELECT MAX(id) FROM {name_app}_{name_model}));")

    def handle(self, *args, **options):
        """Метод для заполнения БД"""
        # таблица contenttypes.contenttype

        ContentType.objects.all().delete()
        Command.truncate_table_restart_id('django', 'content_type')

        contenttype_for_create = []

        for content in Command.json_read_data('contenttypes_data.json', 'contenttypes', 'contenttype'):
            contenttype_for_create.append(
                ContentType(
                    id=content["pk"],
                    app_label=content["fields"]["app_label"],
                    model=content["fields"]["model"])
            )

        ContentType.objects.bulk_create(contenttype_for_create)
        Command.select_setval_id('django', 'content_type')

        # таблица auth.permission

        Permission.objects.all().delete()
        Command.truncate_table_restart_id('auth', 'permission')
        permission_for_create = []

        for perm in Command.json_read_data('auth_data.json', 'auth', 'permission'):
            permission_for_create.append(
                Permission(
                    id=perm["pk"],
                    name=perm["fields"]["name"],
                    content_type=ContentType.objects.get(pk=perm["fields"]["content_type"]),
                    codename=perm["fields"]["codename"],
                )
            )

        Permission.objects.bulk_create(permission_for_create)
        Command.select_setval_id('auth', 'permission')

        # таблица auth.group

        Group.objects.all().delete()
        Command.truncate_table_restart_id('auth', 'group')
        group_for_create = []
        group_permissions = {}

        for group in Command.json_read_data('auth_data.json', 'auth', 'group'):
            permissions = []
            for perm_id in group["fields"]["permissions"]:
                permissions.append(Permission.objects.get(id=perm_id))
            group_permissions[group["pk"]] = permissions

            group_for_create.append(
                Group(
                    id=group["pk"],
                    name=group["fields"]["name"],
                )
            )

        Group.objects.bulk_create(group_for_create)
        Command.select_setval_id('auth', 'group')

        for pk, permissions in group_permissions.items():
            group = Group.objects.get(pk=pk)
            group.permissions.set(permissions)

        # таблица users.user
        User.objects.all().delete()
        Command.truncate_table_restart_id('users', 'user')

        user_for_create = []
        user_groups = {}
        user_permissions = {}
        for user in Command.json_read('users_data.json'):
            permissions = [Permission.objects.get(id=perm_id) for perm_id in user["fields"]["user_permissions"]]
            user_permissions[user["pk"]] = permissions
            groups = [Group.objects.get(pk=group_id) for group_id in user["fields"]["groups"]]
            user_groups[user["pk"]] = groups
            user_for_create.append(
                User(
                    id=user["pk"],
                    password=user["fields"]["password"],
                    last_login=user["fields"]["last_login"],
                    is_superuser=user["fields"]["is_superuser"],
                    is_staff=user["fields"]["is_staff"],
                    is_active=user["fields"]["is_active"],
                    date_joined=user["fields"]["date_joined"],
                    email=user["fields"]["email"],
                    phone_number=user["fields"]["phone_number"],
                    company=user["fields"]["company"],
                    token=user["fields"]["token"],
                    first_name=user["fields"]["first_name"],
                    last_name=user["fields"]["last_name"],
                )
            )

        User.objects.bulk_create(user_for_create)
        Command.select_setval_id('users', 'user')

        for pk, permissions in user_permissions.items():
            user = User.objects.get(pk=pk)
            user.user_permissions.set(permissions)

        for pk, groups in user_groups.items():
            user = User.objects.get(pk=pk)
            user.groups.set(groups)

        BlogPost.objects.all().delete()
        Command.truncate_table_restart_id('blog', 'blogpost')

        blogpost_for_create = []
        for blogpost in Command.json_read('blog_data.json'):
            blogpost_for_create.append(
                BlogPost(id=blogpost["pk"], title=blogpost["fields"]["title"], slug=blogpost["fields"]["slug"],
                         content=blogpost["fields"]["content"], preview=blogpost["fields"]["preview"],
                         is_published=blogpost["fields"]["is_published"],
                         views_count=blogpost["fields"]["views_count"],
                         created_at=blogpost["fields"]["created_at"],
                         author=User.objects.get(pk=blogpost["fields"]["author"])
                         )
            )

        BlogPost.objects.bulk_create(blogpost_for_create)
        Command.select_setval_id('blog', 'blogpost')

        Client.objects.all().delete()
        Command.truncate_table_restart_id('mailing', 'client')

        client_for_create = []
        for client in Command.json_read_data('mailing_data.json', 'mailing', 'client'):
            client_for_create.append(
                Client(
                    id=client["pk"],
                    email=client["fields"]["email"],
                    name=client["fields"]["name"],
                    comments=client["fields"]["comments"],
                    owner=User.objects.get(pk=client["fields"]["owner"])
                )
            )

        Client.objects.bulk_create(client_for_create)
        Command.select_setval_id('mailing', 'client')

        Message.objects.all().delete()
        Command.truncate_table_restart_id('mailing', 'message')

        message_for_create = []
        for message in Command.json_read_data('mailing_data.json', 'mailing', 'message'):
            message_for_create.append(
                Message(
                    id=message["pk"],
                    theme=message["fields"]["theme"],
                    body=message["fields"]["body"],
                    owner=User.objects.get(pk=message["fields"]["owner"])
                )
            )

        Message.objects.bulk_create(message_for_create)
        Command.select_setval_id('mailing', 'message')

        MailingSettings.objects.all().delete()
        Command.truncate_table_restart_id('mailing', 'mailingsettings')

        mailingsettings_for_create = []
        mailing_clients = {}
        for mailing in Command.json_read_data(
                'mailing_data.json',
                'mailing',
                'mailingsettings'
        ):
            clients = [Client.objects.get(pk=client_id) for client_id in mailing["fields"]["clients"]]
            mailing_clients[mailing["pk"]] = clients
            mailingsettings_for_create.append(
                MailingSettings(
                    id=mailing["pk"],
                    start_datetime=mailing["fields"]["start_datetime"],
                    end_datetime=mailing["fields"]["end_datetime"],
                    periodicity=mailing["fields"]["periodicity"],
                    mailing_status=mailing["fields"]["mailing_status"],
                    is_disabled=mailing["fields"]["is_disabled"],
                    message=Message.objects.get(pk=mailing["fields"]["message"]),
                    owner=User.objects.get(pk=mailing["fields"]["owner"])
                )
            )

        MailingSettings.objects.bulk_create(mailingsettings_for_create)
        Command.select_setval_id('mailing', 'mailingsettings')

        for pk, clients in mailing_clients.items():
            mailingsettings = MailingSettings.objects.get(pk=pk)
            mailingsettings.clients.set(clients)

        MailingAttempt.objects.all().delete()
        Command.truncate_table_restart_id('mailing', 'mailingattempt')

        mailingattempt_for_create = []
        for attempt in Command.json_read_data(
                'mailing_data.json',
                'mailing',
                'mailingattempt'
        ):
            mailingattempt_for_create.append(
                MailingAttempt(
                    id=attempt["pk"],
                    datetime_last_try=attempt["fields"]["datetime_last_try"],
                    attempt_status=attempt["fields"]["attempt_status"],
                    response_mail_server=attempt["fields"]["response_mail_server"],
                    mailing=MailingSettings.objects.get(pk=attempt["fields"]["mailing"])
                )
            )

        MailingAttempt.objects.bulk_create(mailingattempt_for_create)
        Command.select_setval_id('mailing', 'mailingattempt')
