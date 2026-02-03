"""Progress URL configuration."""
from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('', views.ProgressListView.as_view(), name='list'),
    path('action/', views.ProgressActionView.as_view(), name='action'),
]
