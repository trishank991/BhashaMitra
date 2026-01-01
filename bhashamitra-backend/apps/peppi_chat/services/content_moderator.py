"""Content moderation service for Peppi chatbot safety."""
import logging
import re
from typing import Tuple, List, Optional

logger = logging.getLogger(__name__)


class ContentModerator:
    """
    Multi-layer content moderation for child-safe AI chat.

    Provides:
    - Input filtering for inappropriate content
    - Personal information detection
    - Output validation
    - Audit logging
    """

    # Blocked patterns - violence, weapons, adult content
    BLOCKED_PATTERNS = {
        'violence': [
            r'\b(kill|murder|die|death|dead|blood|weapon|gun|knife|bomb|fight|hurt|attack)\b',
            r'\b(मारना|मौत|खून|हथियार|बंदूक|चाकू|बम|लड़ाई)\b',  # Hindi
        ],
        'adult_content': [
            r'\b(sex|porn|nude|naked|xxx|adult|drugs|alcohol|beer|wine|whisky)\b',
            r'\b(शराब|नशा|सेक्स)\b',  # Hindi
        ],
        'personal_info': [
            r'\b(password|credit.?card|bank.?account|social.?security)\b',
            r'\b(address|phone.?number|email|school.?name|where.?do.?you.?live)\b',
            r'\b(पासवर्ड|बैंक|पता|फोन.?नंबर)\b',  # Hindi
        ],
        'strangers': [
            r'\b(meet.?me|come.?to|secret|don\'t.?tell|hide)\b',
            r'\b(मिलो|आ जाओ|छुपाओ|किसी को मत बताना)\b',  # Hindi
        ],
    }

    # Patterns for detecting personal information in input
    PERSONAL_INFO_PATTERNS = [
        r'\b\d{10}\b',  # Phone numbers
        r'\b\d{5,6}\b',  # PIN codes
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
        r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',  # Credit card
        r'\b(my.?school.?is|i.?live.?at|my.?address|my.?phone)\b',
    ]

    # Allowed topics for redirection
    ALLOWED_TOPICS = [
        'language learning',
        'vocabulary',
        'grammar',
        'stories',
        'festivals',
        'Indian culture',
        'animals',
        'nature',
        'food',
        'art',
        'music',
        'school',
        'learning',
    ]

    # Safe redirection message
    REDIRECT_MESSAGE = (
        "अरे! Peppi sirf padhai aur kahaniyon ke baare mein baat karta hai! "
        "(I only talk about learning and stories!) "
        "Chalo kuch naya sikhe? 📚"
    )

    @classmethod
    def moderate_input(
        cls,
        content: str,
        child_age: int = 8,
    ) -> Tuple[str, bool, List[str], str]:
        """
        Moderate user input content.

        Args:
            content: The user's message
            child_age: The child's age for age-appropriate filtering

        Returns:
            Tuple of (processed_content, was_modified, matched_patterns, action)
            action: 'ALLOWED', 'MODIFIED', 'BLOCKED', 'FLAGGED'
        """
        matched_patterns = []
        action = 'ALLOWED'
        processed_content = content

        # Check for blocked patterns
        for category, patterns in cls.BLOCKED_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    matched_patterns.append(f"{category}:{pattern}")
                    action = 'BLOCKED'
                    logger.warning(
                        f"Content blocked - category: {category}, "
                        f"pattern: {pattern}"
                    )

        # If blocked, return redirect message
        if action == 'BLOCKED':
            return cls.REDIRECT_MESSAGE, True, matched_patterns, action

        # Check for personal information
        for pattern in cls.PERSONAL_INFO_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                matched_patterns.append(f"personal_info:{pattern}")
                action = 'FLAGGED'
                logger.info(f"Personal info pattern detected: {pattern}")

        # If flagged but not blocked, allow with caution
        if action == 'FLAGGED':
            # Don't modify, but log for review
            return content, False, matched_patterns, action

        return processed_content, False, matched_patterns, action

    @classmethod
    def moderate_output(
        cls,
        content: str,
        child_age: int = 8,
    ) -> Tuple[str, bool, List[str]]:
        """
        Moderate AI output to ensure child-appropriateness.

        Args:
            content: The AI's response
            child_age: The child's age

        Returns:
            Tuple of (processed_content, was_modified, issues_found)
        """
        issues = []
        processed = content

        # Check for any leaked inappropriate content
        for category, patterns in cls.BLOCKED_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    issues.append(f"output_{category}")
                    # Remove the problematic phrase
                    processed = re.sub(pattern, '[...]', processed, flags=re.IGNORECASE)

        was_modified = len(issues) > 0

        if was_modified:
            logger.warning(f"AI output moderated: {issues}")

        return processed, was_modified, issues

    @classmethod
    def detect_off_topic(cls, content: str) -> Tuple[bool, Optional[str]]:
        """
        Detect if the user is trying to discuss off-topic subjects.

        Args:
            content: The user's message

        Returns:
            Tuple of (is_off_topic, suggested_redirect)
        """
        # Keywords that suggest off-topic conversation
        off_topic_indicators = [
            r'\b(video.?game|movie|youtube|tiktok|instagram|facebook)\b',
            r'\b(boyfriend|girlfriend|dating|love|relationship)\b',
            r'\b(politics|election|government|minister)\b',
            r'\b(religion|god|allah|jesus|hindu|muslim)\b',
        ]

        for pattern in off_topic_indicators:
            if re.search(pattern, content, re.IGNORECASE):
                return True, cls.REDIRECT_MESSAGE

        return False, None

    @classmethod
    def get_severity(cls, matched_patterns: List[str]) -> str:
        """
        Determine severity level based on matched patterns.

        Args:
            matched_patterns: List of matched pattern strings

        Returns:
            Severity level: 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
        """
        if not matched_patterns:
            return 'LOW'

        # Check for critical patterns
        critical_categories = ['violence', 'adult_content', 'strangers']
        for pattern in matched_patterns:
            for category in critical_categories:
                if category in pattern:
                    return 'CRITICAL'

        # Check for high severity
        high_categories = ['personal_info']
        for pattern in matched_patterns:
            for category in high_categories:
                if category in pattern:
                    return 'HIGH'

        return 'MEDIUM'

    @classmethod
    def create_safety_log(
        cls,
        conversation,
        child,
        action: str,
        input_content: str,
        output_content: str,
        matched_patterns: List[str],
        reason: str,
    ):
        """
        Create a safety log entry for audit purposes.

        Args:
            conversation: PeppiConversation instance
            child: Child instance
            action: The moderation action taken
            input_content: Original input
            output_content: Modified output (if applicable)
            matched_patterns: List of matched patterns
            reason: Reason for the action
        """
        from apps.peppi_chat.models import PeppiSafetyLog

        severity = cls.get_severity(matched_patterns)

        log = PeppiSafetyLog.objects.create(
            conversation=conversation,
            child=child,
            action=action,
            input_content=input_content,
            output_content=output_content,
            reason=reason,
            matched_patterns=matched_patterns,
            severity=severity,
        )

        logger.info(
            f"Safety log created: {action} - severity: {severity} - "
            f"child: {child.id}"
        )

        return log

    @classmethod
    def check_rate_limit(cls, child, tier: str) -> Tuple[bool, str]:
        """
        Check if the child has exceeded their daily rate limit.

        Args:
            child: Child instance
            tier: Subscription tier (FREE, STANDARD, PREMIUM)

        Returns:
            Tuple of (is_allowed, message)
        """
        from apps.peppi_chat.models import PeppiChatUsage

        # Rate limits by tier
        limits = {
            'FREE': {'messages': 10, 'conversations': 3},  # Limited access for curriculum help
            'STANDARD': {'messages': 50, 'conversations': 10},
            'PREMIUM': {'messages': 200, 'conversations': 100},
        }

        tier_limits = limits.get(tier, limits['FREE'])

        # FREE tier has no access
        if tier_limits['messages'] == 0:
            return False, "Peppi chat is available for paid subscribers only. Upgrade to chat with Peppi!"

        # Get today's usage
        usage = PeppiChatUsage.get_or_create_today(child)

        if usage.messages_sent >= tier_limits['messages']:
            return False, f"You've used all {tier_limits['messages']} messages for today! Come back tomorrow! 🌙"

        if usage.conversations_started >= tier_limits['conversations']:
            return False, "You've started too many conversations today! Let's continue one of them! 💬"

        return True, ""
