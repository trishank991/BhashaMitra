"""Children URL configuration."""
from django.urls import path
from . import views

app_name = 'children'

urlpatterns = [
    path('', views.ChildListCreateView.as_view(), name='list-create'),
    path('<uuid:pk>/', views.ChildDetailView.as_view(), name='detail'),
    path('<uuid:pk>/stats/', views.ChildStatsView.as_view(), name='stats'),
    # Nested curriculum routes
    path('<uuid:child_id>/curriculum/vocabulary/themes/', views.VocabularyThemeListView.as_view(), name='vocabulary-themes'),
    path('<uuid:child_id>/curriculum/vocabulary/themes/<uuid:theme_id>/words/', views.VocabularyThemeWordsView.as_view(), name='vocabulary-theme-words'),
    path('<uuid:child_id>/curriculum/vocabulary/themes/<uuid:theme_id>/stats/', views.VocabularyThemeStatsView.as_view(), name='vocabulary-theme-stats'),
    # Grammar topics
    path('<uuid:child_id>/curriculum/grammar/topics/', views.GrammarTopicListView.as_view(), name='grammar-topics'),
]