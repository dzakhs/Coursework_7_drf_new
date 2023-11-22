from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    place = models.CharField(max_length=100, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=100, verbose_name='действие')
    pleasant_habit = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='связанная привычка')
    frequency = models.IntegerField(default=1, verbose_name='периодичность')
    reward = models.CharField(max_length=100, blank=True, verbose_name='вознаграждение')
    execution_time = models.IntegerField(default=0, verbose_name='продолжительность')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    def __str__(self):
        return self.action

    def clean(self):
        if self.related_habit and self.reward:
            raise ValidationError("Нельзя одновременно выбирать связанную привичку и вознаграждение")

        if self.execution_time > 120:
            raise ValidationError('Продолжительность не может быть больше 120 секунд.')

        if self.related_habit and not self.related_habit.pleasant_habit:
            raise ValidationError('В связанные привычки могут попадать только привычки с признаком приятной привычки.')

        if self.pleasant_habit and (self.reward or self.related_habit):
            raise ValidationError('Приятные привычки могут быть только без вознаграждения и приятной привычки')

        if self.frequency < 7:
            raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней')

    def save(self, *args, **kwargs):
        if self.execution_time == 0:
            self.execution_time = (timezone.datetime.combine(timezone.datetime.today(),
                                                             self.time) - timezone.datetime.now()).seconds
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'