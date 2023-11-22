from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from habit.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        """
        Настройка для тестирования
        """
        self.user = User.objects.create(
            email="test@test.com",
            password="test",
            telegram_username="test",
            is_superuser=False,
            is_staff=False,
            is_active=True,
            )
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(user=self.user, time='15:00:00', action="test", place="test", pleasant_habit=False, frequency=1, reward="test", execution_time=100, is_public=False)

    def test_create_habit(self):
        data = {
            'user': self.user,
            "time": "15:00:00",
            "action": "test",
            "place": "test",
            "pleasant_habit": "False",
            "related_habit": "",
            "frequency": 1,
            "reward": "test",
            "execution_time": 100,
            "is_public": "False"
        }
        response = self.client.post("/habit/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habit.objects.all().exists())

    def test_get_habits(self):
        """
        Тестирование вывода списка привычек
        """
        response = self.client.get(
            reverse('habit:habit-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_habit(self):
        """
        Тестирование обновления привычки
        """
        updata = {
            "action": "test_ok",
        }
        update_url = f"/habit/update/{self.habit.id}/"
        response = self.client.patch(update_url, data=updata)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), {'id': self.habit.id, 'user': self.user.id, 'action': 'test_ok', 'place': 'test'})

    def test_detail_habit(self):
        """
        Тестирование детализации привычки
        """
        response = self.client.get(f'/habit/{self.habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_validate_related_habit_and_reward(self):
        """
        Тест на исключение одновременного выбора связанной привычки и вознаграждения
        """
        data = {
            'user': self.user,
            "time": "15:00:00",
            "action": "test",
            "place": "test",
            "pleasant_habit": "False",
            "related_habit": "test",
            "frequency": 1,
            "reward": "test",
            "execution_time": 100,
            "is_public": "False"
        }
        response = self.client.post(f'/habit/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_time_to_complete(self):
        data = {
            'user': self.user.id,
            "time": "15:00:00",
            "action": "test",
            "place": "test",
            "pleasant_habit": 'False',
            "related_habit": '',
            "frequency": 1,
            "reward": "test",
            "execution_time": 170,
            "is_public": 'False'
        }
        response = self.client.post(f'/habit/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Продолжительность не может быть больше 120 секунд.']}
        )

    def test_validate_periodicity(self):
        data = {
            'user': self.user.id,
            "time": "15:00:00",
            "action": "test",
            "place": "test",
            "pleasant_habit": 'False',
            "related_habit": '',
            "frequency": 8,
            "reward": "test",
            "execution_time": 100,
            "is_public": 'False'
        }
        response = self.client.post(f'/habit/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Нельзя выполнять привычку реже, чем 1 раз в 7 дней']}
        )

    def test_validate_pleasant_habit(self):
        data = {
            'user': self.user.id,
            "time": "15:00:00",
            "action": "test",
            "place": "test",
            "pleasant_habit": 'True',
            "related_habit": '',
            "frequency": 1,
            "reward": "test",
            "execution_time": 100,
            "is_public": 'False'
        }
        response = self.client.post(f'/habit/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Приятные привычки могут быть только без вознаграждения и приятной привычки']}
        )

    def test_validate_reward_related_habit(self):
        data_pleasant = {

            'user': self.user.id,
            "time": "15:00:00",
            "action": "test",
            "place": "test",
            "pleasant_habit": 'True',
            "related_habit": "",
            "frequency": 1,
            "reward": "",
            "execution_time": 100,
            "is_public": 'False'
        }
        data = {

            'user': self.user.id,
            "time": "15:00:00",
            "action": "test",
            "place": "test",
            "pleasant_habit": 'False',
            "related_habit": 10,
            "frequency": 1,
            "reward": "test",
            "execution_time": 100,
            "is_public": 'False'
        }
        self.client.post(f'/habit/create/', data_pleasant)
        response = self.client.post(f'/habit/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Нельзя указывать одновременно связанную привычку и вознаграждение.']}
        )