"""URL configuration for family app."""
from django.urls import path
from . import views

app_name = 'family'

urlpatterns = [
    # Family management
    path('', views.FamilyDetailView.as_view(), name='family-detail'),
    path('create/', views.FamilyCreateView.as_view(), name='family-create'),
    
    # Join/Leave family
    path('join/<str:code>/', views.FamilyJoinView.as_view(), name='family-join'),
    
    # Invite code management
    path('invite-code/', views.FamilyInviteCodeView.as_view(), name='family-invite-code'),
    path('invite-code/refresh/', views.FamilyInviteCodeView.as_view(), name='family-invite-code-refresh'),
    path('invite/<str:code>/', views.FamilyInviteValidateView.as_view(), name='family-invite-validate'),
    
    # Children management
    path('children/', views.FamilyChildrenView.as_view(), name='family-children'),
    
    # Curriculum challenges
    path('challenges/', views.ChallengeListCreateView.as_view(), name='challenge-list-create'),
    path('challenges/<uuid:challenge_id>/', views.ChallengeDetailView.as_view(), name='challenge-detail'),
    path('challenges/<uuid:challenge_id>/start/', views.ChallengeStartView.as_view(), name='challenge-start'),
    path('challenges/<uuid:challenge_id>/submit/', views.ChallengeSubmitAnswerView.as_view(), name='challenge-submit'),
    path('challenges/<uuid:challenge_id>/results/', views.ChallengeResultsView.as_view(), name='challenge-results'),
    path('challenges/<uuid:challenge_id>/questions/', views.ChallengeQuestionsView.as_view(), name='challenge-questions'),
    
    # Child-specific endpoints
    path('children/<uuid:child_id>/challenges/', views.ChildActiveChallengesView.as_view(), name='child-challenges'),
]
