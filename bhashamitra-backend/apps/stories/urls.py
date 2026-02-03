"""Story URL configuration."""
from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('', views.StoryListView.as_view(), name='list'),
    path('<uuid:pk>/', views.StoryDetailView.as_view(), name='detail'),
]
