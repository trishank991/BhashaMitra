"""
Challenge URL Configuration.

Public endpoints (no auth):
- GET/POST /play/<code>/    - Get challenge info / Start attempt
- POST     /submit/         - Submit answers
- GET      /leaderboard/<code>/ - Get leaderboard

Authenticated endpoints:
- GET/POST /                - List/Create challenges
- GET      /<code>/         - Get challenge detail
- GET      /quota/          - Get user quota
- GET      /categories/     - Get available categories
"""

from django.urls import path
from . import views

app_name = 'challenges'

urlpatterns = [
    # Public endpoints - Anyone can play!
    path('play/<str:code>/', views.play_challenge, name='play'),
    path('submit/', views.submit_challenge, name='submit'),
    path('leaderboard/<str:code>/', views.challenge_leaderboard, name='leaderboard'),

    # Authenticated endpoints - For creators
    path('', views.challenges_list_create, name='list-create'),
    path('quota/', views.user_quota, name='quota'),
    path('categories/', views.available_categories, name='categories'),
    path('<str:code>/', views.challenge_detail, name='detail'),
]
