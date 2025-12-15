"""Children URL configuration."""
from django.urls import path
from . import views

app_name = 'children'

urlpatterns = [
    path('', views.ChildListCreateView.as_view(), name='list-create'),
    path('<uuid:pk>/', views.ChildDetailView.as_view(), name='detail'),
    path('<uuid:pk>/stats/', views.ChildStatsView.as_view(), name='stats'),
]
