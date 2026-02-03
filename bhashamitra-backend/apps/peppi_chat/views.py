"""API views for Peppi Chat."""
import logging

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from apps.children.models import Child

from .models import (
    PeppiConversation,
    PeppiChatMessage,
    PeppiChatUsage,
    PeppiEscalationReport,
    ChatMode,
    MessageRole,
    InputType,
)
from .serializers import (
    PeppiConversationSerializer,
    PeppiConversationListSerializer,
    PeppiChatMessageSerializer,
    PeppiEscalationReportSerializer,
    StartConversationSerializer,
    SendMessageSerializer,
    SendVoiceMessageSerializer,
    SubmitEscalationSerializer,
)
from .services import (
    GeminiAIService,
    ContentModerator,
    ContextBuilder,
    PromptTemplates,
)

logger = logging.getLogger(__name__)


class PeppiChatViewSet(ViewSet):
    """
    ViewSet for Peppi AI Chat operations.

    Provides endpoints for:
    - Starting conversations
    - Sending messages
    - Getting conversation history
    - Ending conversations
    """

    permission_classes = [IsAuthenticated]

    def get_child(self, request, child_id):
        """Get child and verify access."""
        # child_id comes from URL as UUID
        child = get_object_or_404(Child, id=child_id)

        # Verify the user owns this child profile
        if child.user != request.user:
            return None, Response(
                {'error': 'You do not have access to this child profile'},
                status=status.HTTP_403_FORBIDDEN
            )

        return child, None

    def get_child_age(self, child):
        """Get child's age from date of birth."""
        from datetime import date
        if hasattr(child, 'date_of_birth') and child.date_of_birth:
            today = date.today()
            return today.year - child.date_of_birth.year - (
                (today.month, today.day) < (child.date_of_birth.month, child.date_of_birth.day)
            )
        return 8  # Default age

    def check_tier_access(self, user, mode: str = None) -> tuple:
        """Check if user's tier allows Peppi chat access.

        FREE tier: Only CURRICULUM_HELP mode with preset prompts (restricted)
        PAID tiers: All modes with full chat capabilities
        """
        # Get user's subscription tier
        tier = getattr(user, 'subscription_tier', 'FREE')
        if hasattr(user, 'get_subscription_tier'):
            tier = user.get_subscription_tier()

        # FREE tier can ONLY use CURRICULUM_HELP mode (for preset prompts)
        if tier == 'FREE':
            if mode == 'CURRICULUM_HELP':
                # Allow limited access for curriculum help with preset prompts
                return True, 'FREE'
            else:
                return False, "Full Peppi chat is available for paid subscribers only. Upgrade to unlock all modes!"

        return True, tier

    @action(detail=False, methods=['post'], url_path='start')
    def start_conversation(self, request, child_id=None):
        """
        Start a new Peppi chat conversation.

        POST /api/children/{child_id}/peppi-chat/start/
        """
        child, error = self.get_child(request, child_id)
        if error:
            return error

        # Parse request data first to get the mode
        serializer = StartConversationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        mode = data.get('mode', ChatMode.GENERAL)
        language = data.get('language', 'HINDI')

        # Check tier access with mode (FREE users can only use CURRICULUM_HELP)
        has_access, tier_or_msg = self.check_tier_access(request.user, mode=mode)
        if not has_access:
            return Response(
                {'error': tier_or_msg},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check rate limits
        is_allowed, limit_msg = ContentModerator.check_rate_limit(child, tier_or_msg)
        if not is_allowed:
            return Response(
                {'error': limit_msg},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Get optional context references
        festival = None
        story = None
        lesson = None

        if mode == ChatMode.FESTIVAL_STORY:
            from apps.festivals.models import Festival
            from apps.stories.models import Story
            # Festival and story are optional for general story chat
            if data.get('festival_id'):
                try:
                    festival = Festival.objects.get(id=data['festival_id'])
                except (Festival.DoesNotExist, ValueError):
                    festival = None
            if data.get('story_id'):
                try:
                    story = Story.objects.get(id=data['story_id'])
                except (Story.DoesNotExist, ValueError):
                    story = None

        elif mode == ChatMode.CURRICULUM_HELP and data.get('lesson_id'):
            from apps.curriculum.models import Lesson
            lesson = get_object_or_404(Lesson, id=data['lesson_id'])

        # Create conversation
        conversation = PeppiConversation.objects.create(
            child=child,
            mode=mode,
            language=language,
            festival=festival,
            story=story,
            lesson=lesson,
            context_snapshot={'current_page': 1} if mode == ChatMode.FESTIVAL_STORY else {},
        )

        # Update usage
        usage = PeppiChatUsage.get_or_create_today(child)
        usage.increment_conversations()

        # Generate initial greeting in the child's learning language
        time_of_day = ContextBuilder.get_time_of_day()
        greeting = PromptTemplates.get_greeting(child.name, time_of_day, language)

        # Add greeting as first assistant message
        greeting_msg = PeppiChatMessage.objects.create(
            conversation=conversation,
            role=MessageRole.ASSISTANT,
            content_primary=greeting,
        )

        conversation.messages_count = 1
        conversation.save(update_fields=['messages_count'])

        logger.info(
            f"Peppi conversation started: child={child.id}, mode={mode}, "
            f"conversation={conversation.id}"
        )

        return Response({
            'conversation': PeppiConversationSerializer(conversation).data,
            'greeting': PeppiChatMessageSerializer(greeting_msg).data,
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='messages')
    def send_message(self, request, child_id=None, pk=None):
        """
        Send a message in an existing conversation.

        POST /api/children/{child_id}/peppi-chat/{conversation_id}/messages/
        """
        child, error = self.get_child(request, child_id)
        if error:
            return error

        conversation = get_object_or_404(
            PeppiConversation,
            id=pk,
            child=child,
            is_active=True
        )

        # Check tier access with conversation mode (FREE users can only use CURRICULUM_HELP)
        has_access, tier_or_msg = self.check_tier_access(request.user, mode=conversation.mode)
        if not has_access:
            return Response(
                {'error': tier_or_msg},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check rate limits
        is_allowed, limit_msg = ContentModerator.check_rate_limit(child, tier_or_msg)
        if not is_allowed:
            return Response(
                {'error': limit_msg},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        serializer = SendMessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_content = serializer.validated_data['content']
        input_type = serializer.validated_data.get('input_type', InputType.TEXT)
        audio_url = serializer.validated_data.get('audio_url', '')

        # Moderate input
        child_age = self.get_child_age(child)
        moderated_content, was_modified, patterns, action = ContentModerator.moderate_input(
            user_content,
            child_age
        )

        # Log if content was blocked or flagged
        if action in ['BLOCKED', 'FLAGGED']:
            ContentModerator.create_safety_log(
                conversation=conversation,
                child=child,
                action=action,
                input_content=user_content,
                output_content=moderated_content if was_modified else '',
                matched_patterns=patterns,
                reason=f"Content moderation: {action}",
            )

        # If blocked, return the redirect message directly
        if action == 'BLOCKED':
            # Still save the user message (with original content marked as moderated)
            user_msg = PeppiChatMessage.objects.create(
                conversation=conversation,
                role=MessageRole.USER,
                content_primary=moderated_content,
                input_type=input_type,
                audio_input_url=audio_url,
                was_moderated=True,
                original_content=user_content,
            )

            # Return the moderation message as assistant response
            assistant_msg = PeppiChatMessage.objects.create(
                conversation=conversation,
                role=MessageRole.ASSISTANT,
                content_primary=moderated_content,
            )

            conversation.messages_count += 2
            conversation.save(update_fields=['messages_count', 'last_message_at'])

            return Response({
                'user_message': PeppiChatMessageSerializer(user_msg).data,
                'assistant_message': PeppiChatMessageSerializer(assistant_msg).data,
                'was_moderated': True,
            })

        # Save user message
        user_msg = PeppiChatMessage.objects.create(
            conversation=conversation,
            role=MessageRole.USER,
            content_primary=user_content,
            input_type=input_type,
            audio_input_url=audio_url,
            was_moderated=was_modified,
            original_content=user_content if was_modified else '',
        )

        # Build context and system prompt
        context = ContextBuilder.build_conversation_context(conversation, child)

        # Get Peppi settings from child model
        peppi_gender = getattr(child, 'peppi_gender', 'FEMALE').lower()
        addressing_mode = getattr(child, 'peppi_addressing', 'BY_NAME')

        system_prompt = PromptTemplates.build_system_prompt(
            mode=conversation.mode,
            child_name=child.name,
            child_age=child_age,
            peppi_gender=peppi_gender,
            addressing_mode=addressing_mode,
            language=conversation.language,
            context=context,
        )

        logger.info(
            f"Peppi chat request: child={child.id}, mode={conversation.mode}, "
            f"language={conversation.language}, system_prompt_length={len(system_prompt)}"
        )

        # Generate AI response (synchronous for now)
        try:
            response_text, token_count, latency_ms = GeminiAIService.generate_response_sync(
                conversation=conversation,
                user_message=user_content,
                system_prompt=system_prompt,
                language=conversation.language,
            )
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            response_text = "अरे! Peppi को कुछ problem हो गई। 😅 Ek minute mein phir try karo!"
            token_count = 0
            latency_ms = 0

        # Check for escalation flag
        needs_escalation = '[NEEDS_ESCALATION]' in response_text
        if needs_escalation:
            # Strip the escalation flag from the response
            response_text = response_text.replace('[NEEDS_ESCALATION]', '').strip()

        # Moderate output
        safe_response, output_modified, output_issues = ContentModerator.moderate_output(
            response_text,
            child_age
        )

        if output_modified:
            ContentModerator.create_safety_log(
                conversation=conversation,
                child=child,
                action='MODIFIED',
                input_content=response_text,
                output_content=safe_response,
                matched_patterns=output_issues,
                reason="AI output moderation",
            )

        # Save assistant message
        assistant_msg = PeppiChatMessage.objects.create(
            conversation=conversation,
            role=MessageRole.ASSISTANT,
            content_primary=safe_response,
            token_count=token_count,
            latency_ms=latency_ms,
            was_moderated=output_modified,
            original_content=response_text if output_modified else '',
        )

        # Update conversation stats
        conversation.messages_count += 2
        conversation.total_tokens_used += token_count
        conversation.save(update_fields=['messages_count', 'total_tokens_used', 'last_message_at'])

        # Update daily usage
        usage = PeppiChatUsage.get_or_create_today(child)
        usage.messages_sent += 1
        usage.tokens_used += token_count
        if input_type == InputType.VOICE:
            usage.voice_messages_sent += 1
        usage.save()

        logger.info(
            f"Peppi message: conv={conversation.id}, tokens={token_count}, "
            f"latency={latency_ms}ms, needs_escalation={needs_escalation}"
        )

        return Response({
            'user_message': PeppiChatMessageSerializer(user_msg).data,
            'assistant_message': PeppiChatMessageSerializer(assistant_msg).data,
            'was_moderated': was_modified or output_modified,
            'needs_escalation': needs_escalation,
        })

    @action(detail=True, methods=['get'], url_path='history')
    def get_history(self, request, child_id=None, pk=None):
        """
        Get conversation history.

        GET /api/children/{child_id}/peppi-chat/{conversation_id}/history/
        """
        child, error = self.get_child(request, child_id)
        if error:
            return error

        conversation = get_object_or_404(
            PeppiConversation,
            id=pk,
            child=child
        )

        # Pagination
        limit = int(request.query_params.get('limit', 50))
        offset = int(request.query_params.get('offset', 0))

        messages = conversation.messages.order_by('created_at')[offset:offset + limit]
        total = conversation.messages.count()

        return Response({
            'conversation': PeppiConversationListSerializer(conversation).data,
            'messages': PeppiChatMessageSerializer(messages, many=True).data,
            'has_more': (offset + limit) < total,
            'total_messages': total,
        })

    @action(detail=True, methods=['post'], url_path='end')
    def end_conversation(self, request, child_id=None, pk=None):
        """
        End a conversation.

        POST /api/children/{child_id}/peppi-chat/{conversation_id}/end/
        """
        child, error = self.get_child(request, child_id)
        if error:
            return error

        conversation = get_object_or_404(
            PeppiConversation,
            id=pk,
            child=child,
            is_active=True
        )

        conversation.end_conversation()

        logger.info(f"Peppi conversation ended: {conversation.id}")

        return Response({
            'message': 'Conversation ended',
            'conversation': PeppiConversationListSerializer(conversation).data,
        })

    @action(detail=False, methods=['get'], url_path='list')
    def list_conversations(self, request, child_id=None):
        """
        List all conversations for a child.

        GET /api/children/{child_id}/peppi-chat/list/
        """
        child, error = self.get_child(request, child_id)
        if error:
            return error

        # Filter options
        active_only = request.query_params.get('active', 'false').lower() == 'true'
        mode = request.query_params.get('mode', None)

        conversations = PeppiConversation.objects.filter(child=child)

        if active_only:
            conversations = conversations.filter(is_active=True)

        if mode and mode in [c[0] for c in ChatMode.choices]:
            conversations = conversations.filter(mode=mode)

        conversations = conversations.order_by('-last_message_at')[:20]

        return Response({
            'conversations': PeppiConversationListSerializer(conversations, many=True).data,
        })

    @action(detail=True, methods=['post'], url_path='escalate')
    def submit_escalation(self, request, child_id=None, pk=None):
        """
        Submit an escalation report when Peppi cannot help.

        POST /api/children/{child_id}/peppi-chat/{conversation_id}/escalate/
        """
        child, error = self.get_child(request, child_id)
        if error:
            return error

        conversation = get_object_or_404(
            PeppiConversation,
            id=pk,
            child=child
        )

        serializer = SubmitEscalationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Get the message if provided
        message = None
        if data.get('message_id'):
            message = PeppiChatMessage.objects.filter(
                id=data['message_id'],
                conversation=conversation
            ).first()

        # Create escalation report
        escalation = PeppiEscalationReport.objects.create(
            conversation=conversation,
            child=child,
            message=message,
            user_description=data['description'],
            mode=conversation.mode,
        )

        logger.info(
            f"Escalation submitted: child={child.id}, conv={conversation.id}, "
            f"escalation={escalation.id}"
        )

        return Response({
            'escalation': PeppiEscalationReportSerializer(escalation).data,
            'message': 'Your report has been submitted. Our team will look into it!',
        }, status=status.HTTP_201_CREATED)


class PeppiChatStatusView(APIView):
    """View to check Peppi chat service status."""

    permission_classes = [IsAuthenticated]

    def get(self, request, child_id=None):
        """Check if Peppi chat is available.

        FREE tier: Limited access (CURRICULUM_HELP mode only with preset prompts)
        PAID tiers: Full access to all modes
        """
        gemini_available = GeminiAIService.is_available()

        # Get user's subscription tier
        tier = getattr(request.user, 'subscription_tier', 'FREE')
        if hasattr(request.user, 'get_subscription_tier'):
            tier = request.user.get_subscription_tier()

        # FREE tier has LIMITED access (CURRICULUM_HELP only)
        # PAID tiers have FULL access
        is_free_tier = tier == 'FREE'

        # Determine appropriate message
        if not gemini_available:
            message = "Peppi is taking a short nap. Please try again in a moment! 😴"
        elif is_free_tier:
            message = "Peppi is ready to help with your lessons!"
        else:
            message = "Peppi is ready to chat!"

        return Response({
            # FREE tier can use CURRICULUM_HELP mode (limited access)
            # So we return available=True if gemini is up
            'available': gemini_available,
            'gemini_status': 'online' if gemini_available else 'offline',
            'tier_access': True,  # All tiers have some access now
            'tier': tier,
            'is_limited': is_free_tier,  # Flag for frontend to know it's limited
            'message': message,
        })
