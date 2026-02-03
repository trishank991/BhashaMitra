"""URL configuration for Peppi Chat API."""
from django.urls import path

from .views import PeppiChatViewSet, PeppiChatStatusView

app_name = 'peppi_chat'

# Create viewset actions as views
peppi_chat_viewset = PeppiChatViewSet.as_view({
    'post': 'start_conversation',
    'get': 'list_conversations',
})

peppi_chat_detail_viewset = PeppiChatViewSet.as_view({
    'get': 'get_history',
    'delete': 'end_conversation',
})

peppi_chat_messages_viewset = PeppiChatViewSet.as_view({
    'post': 'send_message',
})

peppi_chat_end_viewset = PeppiChatViewSet.as_view({
    'post': 'end_conversation',
})

# These URLs are nested under /api/v1/children/<uuid:child_id>/peppi-chat/
# The child_id is captured by this URL pattern prefix
urlpatterns = [
    # Peppi chat status (child-specific for tier checking)
    # GET /api/v1/children/{child_id}/peppi-chat/status/
    path(
        'status/',
        PeppiChatStatusView.as_view(),
        name='peppi-chat-status'
    ),

    # Start new conversation / List conversations
    # GET /api/v1/children/{child_id}/peppi-chat/
    # POST /api/v1/children/{child_id}/peppi-chat/
    path(
        '',
        peppi_chat_viewset,
        name='peppi-chat-list'
    ),

    # Conversation history
    # GET /api/v1/children/{child_id}/peppi-chat/{conversation_id}/
    path(
        '<uuid:pk>/',
        peppi_chat_detail_viewset,
        name='peppi-chat-detail'
    ),

    # Send message
    # POST /api/v1/children/{child_id}/peppi-chat/{conversation_id}/messages/
    path(
        '<uuid:pk>/messages/',
        peppi_chat_messages_viewset,
        name='peppi-chat-messages'
    ),

    # End conversation
    # POST /api/v1/children/{child_id}/peppi-chat/{conversation_id}/end/
    path(
        '<uuid:pk>/end/',
        peppi_chat_end_viewset,
        name='peppi-chat-end'
    ),

    # Escalation
    # POST /api/v1/children/{child_id}/peppi-chat/{conversation_id}/escalate/
    path(
        '<uuid:pk>/escalate/',
        PeppiChatViewSet.as_view({'post': 'submit_escalation'}),
        name='peppi-chat-escalate'
    ),
]