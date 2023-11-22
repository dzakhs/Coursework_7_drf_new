from django.urls import path

from habit.apps import HabitConfig
from habit.views import HabitCreateAPIView, HabitRetrieveAPIView, HabitUpdateAPIView, HabitDestroyAPIView, \
    PublicHabitListAPIView, HabitListAPIView

app_name = HabitConfig.name

urlpatterns = [
    path('habit/create/', HabitCreateAPIView.as_view(), name='habit-create'),
    path('habits/', HabitListAPIView.as_view(), name='habit-list'),
    path('habit/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit-get'),
    path('habit/update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit-update'),
    path('habit/delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit-delete'),
    path('public_habit/', PublicHabitListAPIView.as_view(), name='public-habits'),

]