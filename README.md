# Cервис управления рассылками, администрирования и получения статистики

После создания новой рассылки, если текущие дата и время больше даты и времени начала и меньше даты и времени окончания,
выбираются из справочника клиенты, которые указаны в настройках рассылки и запучкается отправка для всех этих
клиентов.
Если рассылка создана со временем старта в будущем, отправка должна стартовать автоматически по наступлению этого
времени без дополнительных действий со стороны пользователя сервиса.
По ходу отправки рассылки собирается статистика по каждой рассылке для последующего формирования отчетов.

Инструкции по установке
------------

1. Клонировать репозиторий
   ```sh
   git clone https://github.com/MarinaKrasnoruzhskaya/mailing_service
   ```
2. Перейти в директорию mailing_service
   ```sh
   cd mailing_service
   ```
3. Установить Poetry
   ```sh
    pip install poetry
   ```
4. Инициализировать Poetry
   ```sh
   poetry init
   ```
5. Установить зависимости
   ```sh
   poetry install
   ```
6. Обновить зависимости
   ```sh
   poetry update
   ```
7. Создать файл ```.env``` следующего содержания:
   ```
   DB_USER=local_db_user
   DB_PASSWORD=local_db_password
   DB_HOST=local_db_host
   DB_PORT=local_db_port
   EMAIL_HOST_USER = your_email@yandex.ru
   EMAIL_HOST_PASSWORD = your_yandex_smtp_password
   EMAIL_USER = user_email@yandex.ru
   ```
8. Создать БД ```mailing```
   ```
   psql -U postgres
   create database mailing;  
   \q
   ```
9. Применить миграции
    ```sh
   python manage.py migrate
    ```
10. Заполнить БД
   ```sh
   python manage.py fill
   ```

Руководство по использованию
---------------

1. Для запуска проекта в терминале IDE выполнить команду:
  ```sh
   python manage.py runserver
   ```
2. После запуска сервера перейдите по ссылке http://127.0.0.1:8000/ и будет отображена домашняя страница проекта. На
   домашней странице представлен список рассылок

Управление попытками рассылок
---------------

Реализовано несколько способов:
1. Для ```crontab``` добавить задание командой:
   ```shell
   python manage.py crontab add
   ```
2. Для ```APScheduler``` из командной строки выполнить команду
  ```sh
   python manage.py runapscheduler
   ```
   или в файле ```mailing/app.py``` сделать активными строки 10-13 и выполнить команду
```sh
   python manage.py runserver
   ```

Управление проектом
---------------

1. Для создания суперпользователя

  ```sh
   python manage.py createsuperuser
   ```

2. Для перехода в административную панель воспользуйтесь ссылкой http://127.0.0.1:8000/admin/

Пользователи:
admin@mailing.com (admin123)
manager@mailing.com (manager123)
content@mailing.com (content123)
krasnoruzhskayamarina@yandex.ru (cktcfhm1985)

Построен с:
---------------

1. Python 3.12
2. Poetry 1.8.3
3. Django 5.0.6
4. UIkit Bootstrap 5.3
5. Python-dotenv 1.0.1
6. Psycopg2-bynary 2.9.9
7. Pillow 10.4.0
8. Pytz 2024.1
9. Django-crontab 0.7.1
10. Django-apscheduler 0.6.2
11. ipython 8.26.0

[//]: # (9. pytils 0.4.1)

Контакты
---------------
Марина Красноружская - krasnoruzhskayamarina@yandex.ru

Ссылка на
проект: [https://github.com/MarinaKrasnoruzhskaya/django_shop](https://github.com/MarinaKrasnoruzhskaya/django_shop)

<p align="right">(<a href="#readme-top">Наверх</a>)</p>

