from celery import shared_task
from django.conf import settings
import requests
from django.utils import timezone
from datetime import timedelta

from habit.models import Habit


def send_message_tg(telegram_username, time, place, action):
    """
    Функция отправки уведомления в телеграмм
    """
    TOKEN = settings.TELEGRAM_BOT_TOKEN
    get_id_url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'  # Получение chat_id по username
    response = requests.get(get_id_url)
    data = response.json()
    chat_id = None
    for update in data['result']:
        if 'message' in update and 'username' in update['message']['chat']:
            if update['message']['chat']['username'] == telegram_username:
                chat_id = update['message']['chat']['id']
                break
    if chat_id is not None:  # Отправка сообщения в телеграмм
        message = f"СЕГОДНЯ Я буду {action} в {time} в {place}!"
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}'
        response = requests.get(url)
        if response.status_code == 200:
            print("Сообщение успешно отправлено.")
        else:
            print("Ошибка при отправке сообщения.")
    else:
        print("Chat ID для указанного username не найден.")


@shared_task
def check_habit():
    """
    Функция проверки даты и времени для отправки уведомления
    """
    current_time = timezone.now().time()
    current_date = timezone.now().date()
    habits_today = Habit.objects.filter(
        send_date=current_date
    )
    for habit in habits_today:
        if habit.send_time.hour <= current_time.hour and habit.send_time.minute <= current_time.minute:
            send_message_tg(habit.user.telegram_username, habit.time, habit.place, habit.action)
            new_send_date = habit.send_date + timedelta(days=habit.frequency)  # Обновляем send_date у привычки
            habit.send_date = new_send_date
            habit.save()
