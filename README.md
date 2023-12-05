# Coursework_7_drf_new
## Проект по джанго: бэкенд SPA-приложения.

### Для запуска проекта:
1. Клонируем репозиторий
2. Устанавливаем зависимости: pip install -r requirements.txt
3. Подготавливаем файл .env по образу .env.sample
4. Создаем базу данных postgres
5. Подготавливаем миграции (python manage.py makemigrations)
6. Выполняем миграции (python manage.py migrate)
7. Интегрируем сервис с Telegram мессенджером
8. Проходим в телеграмм бот и выполняем команду \start
9. Для запуска сервиса выполняем команды:
   + celery -A Coursework_7_drf worker -l INFO -P eventlet
   + celery -A Coursework_7_drf beat -l info -S django
   + python manage.py runserver

### Для запуска проекта через Docker:
1. Клонируем проект с GitHub
2. Создаем файл .env по форме .env.sample
3. В терминале пишем команду docker-compose build
4. Далее выполняем docker-compose-up 

