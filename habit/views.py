from django.shortcuts import render
from rest_framework import generics

from habit.models import Habit
from habit.pagination import HabitPagination
from habit.permissions import IsOwner, IsCreatorOrStaff
from habit.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт по созданию привычки
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


class HabitListAPIView(generics.ListAPIView):
    """
    Эндпоинт по просмотру привычек
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Habit.objects.all()
        else:
            queryset = Habit.objects.filter(user=self.request.user)
        return queryset


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    Эндпоинт по просмотру привычки
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsCreatorOrStaff]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    Эндпоинт по обновлению привычки
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsCreatorOrStaff]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """
    Эндпоинт по удалению привычки
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


class PublicHabitListAPIView(generics.ListAPIView):
    """
    Эндпоинт по публичным привычкам
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPagination

    def get_queryset(self):
        public_habits = Habit.objects.filter(public=True)
        return public_habits
