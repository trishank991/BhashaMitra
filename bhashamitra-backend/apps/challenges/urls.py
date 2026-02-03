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
    # Public endpoints
    path('play/<str:code>/', views.play_challenge, name='play-challenge'),
    path('submit/', views.submit_challenge, name='submit-challenge'),
    path('leaderboard/<str:code>/', views.challenge_leaderboard, name='challenge-leaderboard'),

    # Authenticated endpoints
    path('', views.challenges_list_create, name='challenges-list-create'),
    path('quota/', views.user_quota, name='user-quota'),
    path('categories/', views.available_categories, name='available-categories'),
    path('languages/', views.available_languages, name='available-languages'),
    path('<str:code>/', views.challenge_detail, name='challenge-detail'),
]
