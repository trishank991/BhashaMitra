"""Gamification URL configuration."""
from django.urls import path
from . import views

app_name = 'gamification'

urlpatterns = [
    path('badges/', views.BadgeListView.as_view(), name='badges'),
    path('streak/', views.StreakView.as_view(), name='streak'),
    path('level/', views.LevelView.as_view(), name='level'),
    path('recordings/', views.RecordingListView.as_view(), name='recordings'),
]
