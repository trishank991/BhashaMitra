"""Google Gemini AI Service for Peppi chatbot."""
import logging
import time
from typing import AsyncGenerator, Optional

from django.conf import settings

logger = logging.getLogger(__name__)


class GeminiAIService:
    """
    Service for Google Gemini AI integration.

    Handles:
    - API communication with Gemini
    - Message history management
    - Streaming responses
    - Token counting and cost tracking
    """

    # Get model settings from Django settings with defaults
    @classmethod
    def get_model_id(cls):
        return getattr(settings, 'GEMINI_MODEL_ID', 'gemini-2.0-flash-exp')

    @classmethod
    def get_max_tokens(cls):
        return getattr(settings, 'PEPPI_CHAT_MAX_TOKENS', 1024)

    @classmethod
    def get_temperature(cls):
        return getattr(settings, 'PEPPI_CHAT_TEMPERATURE', 0.7)

    TOP_P = 0.9
    TOP_K = 40

    # Language code mapping
    LANGUAGE_CODES = {
        'HINDI': 'hi',
        'TAMIL': 'ta',
        'TELUGU': 'te',
        'GUJARATI': 'gu',
        'PUNJABI': 'pa',
        'MALAYALAM': 'ml',
        'BENGALI': 'bn',
        'MARATHI': 'mr',
        'KANNADA': 'kn',
        'ODIA': 'or',
        'FIJI_HINDI': 'hif',  # Fiji Hindi ISO 639-3 code
    }

    _client = None

    @classmethod
    def get_client(cls):
        """
        Get or create the Gemini client.

        Returns:
            GenerativeModel: The Gemini model instance
        """
        if cls._client is None:
            try:
                import google.generativeai as genai

                api_key = getattr(settings, 'GOOGLE_GEMINI_API_KEY', None)
                if not api_key:
                    logger.error("GOOGLE_GEMINI_API_KEY is not set in settings")
                    raise ValueError("GOOGLE_GEMINI_API_KEY not configured")

                logger.info(f"Configuring Gemini with API key (first 8 chars): {api_key[:8]}...")
                genai.configure(api_key=api_key)

                # Configure safety settings for child-appropriate content
                safety_settings = [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_LOW_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_LOW_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_LOW_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_LOW_AND_ABOVE"
                    },
                ]

                # Configure generation settings
                generation_config = {
                    "temperature": cls.get_temperature(),
                    "top_p": cls.TOP_P,
                    "top_k": cls.TOP_K,
                    "max_output_tokens": cls.get_max_tokens(),
                }

                model_id = cls.get_model_id()
                cls._client = genai.GenerativeModel(
                    model_name=model_id,
                    safety_settings=safety_settings,
                    generation_config=generation_config,
                )

                logger.info(f"Gemini client initialized with model: {model_id}")

            except ImportError:
                logger.error("google-generativeai package not installed")
                raise ImportError("Please install google-generativeai: pip install google-generativeai")

        return cls._client

    @classmethod
    def build_messages_history(
        cls,
        conversation,
        max_messages: int = 20,
        include_system_prompt: bool = False,
        system_prompt: str = ""
    ) -> list:
        """
        Build message history for the conversation.

        Args:
            conversation: PeppiConversation instance
            max_messages: Maximum number of messages to include
            include_system_prompt: Whether to include system prompt as first message
            system_prompt: The system prompt to include

        Returns:
            List of message dictionaries for Gemini
        """
        from apps.peppi_chat.models import PeppiChatMessage

        messages = PeppiChatMessage.objects.filter(
            conversation=conversation
        ).order_by('-created_at')[:max_messages]

        # Reverse to get chronological order
        messages = list(reversed(messages))

        history = []

        # Add system prompt as first user message if requested
        if include_system_prompt and system_prompt:
            history.append({
                "role": "user",
                "parts": [system_prompt]
            })
            # Add a brief acknowledgment from model
            history.append({
                "role": "model",
                "parts": ["I understand! I am Peppi, and I will follow these instructions carefully. Ready to help!"]
            })

        for msg in messages:
            if msg.role == 'user':
                history.append({
                    "role": "user",
                    "parts": [msg.content_primary]
                })
            elif msg.role == 'assistant':
                history.append({
                    "role": "model",
                    "parts": [msg.content_primary]
                })

        return history

    @classmethod
    async def generate_response(
        cls,
        conversation,
        user_message: str,
        system_prompt: str,
        language: str = 'HINDI',
        stream: bool = False,
    ) -> AsyncGenerator[str, None]:
        """
        Generate a response from Gemini.

        Args:
            conversation: PeppiConversation instance
            user_message: The user's message
            system_prompt: The system prompt with Peppi personality
            language: The response language
            stream: Whether to stream the response

        Yields:
            Response chunks (if streaming) or full response
        """
        start_time = time.time()

        try:
            model = cls.get_client()

            # Build conversation history with system prompt included
            history = cls.build_messages_history(
                conversation,
                include_system_prompt=True,
                system_prompt=system_prompt
            )

            # Start a chat session with history (which now includes system prompt)
            chat = model.start_chat(history=history)

            # Just send the user message - system prompt is already in history
            full_message = user_message

            if stream:
                # Streaming response
                response = await chat.send_message_async(
                    full_message,
                    stream=True
                )

                full_text = ""
                async for chunk in response:
                    if chunk.text:
                        full_text += chunk.text
                        yield chunk.text

                # Log completion
                latency_ms = int((time.time() - start_time) * 1000)
                logger.info(
                    f"Gemini streaming response completed: "
                    f"{len(full_text)} chars, {latency_ms}ms"
                )

            else:
                # Non-streaming response
                response = await chat.send_message_async(full_message)

                latency_ms = int((time.time() - start_time) * 1000)
                logger.info(
                    f"Gemini response: {len(response.text)} chars, {latency_ms}ms"
                )

                yield response.text

        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            # Return a friendly error message in Hindi
            error_msg = (
                "अरे! Peppi को कुछ problem हो गई। 😅 "
                "Ek minute mein phir try karo!"
            )
            yield error_msg

    @classmethod
    def generate_response_sync(
        cls,
        conversation,
        user_message: str,
        system_prompt: str,
        language: str = 'HINDI',
    ) -> tuple[str, int, int]:
        """
        Generate a response synchronously (non-streaming).

        Args:
            conversation: PeppiConversation instance
            user_message: The user's message
            system_prompt: The system prompt
            language: Response language

        Returns:
            Tuple of (response_text, token_count, latency_ms)
        """
        start_time = time.time()

        try:
            model = cls.get_client()

            # Build conversation history with system prompt included
            history = cls.build_messages_history(
                conversation,
                include_system_prompt=True,
                system_prompt=system_prompt
            )

            # Start chat with history (which now includes system prompt)
            chat = model.start_chat(history=history)

            # Just send the user message - system prompt is already in history
            full_message = user_message

            response = chat.send_message(full_message)

            latency_ms = int((time.time() - start_time) * 1000)

            # Estimate token count (rough approximation)
            token_count = len(response.text.split()) * 2

            logger.info(
                f"Gemini sync response: {len(response.text)} chars, "
                f"~{token_count} tokens, {latency_ms}ms"
            )

            return response.text, token_count, latency_ms

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            logger.error(f"Gemini API error: {str(e)}")
            logger.error(f"Gemini API full traceback:\n{error_details}")
            latency_ms = int((time.time() - start_time) * 1000)
            error_msg = (
                "अरे! Peppi को कुछ problem हो गई। 😅 "
                "Ek minute mein phir try karo!"
            )
            return error_msg, 0, latency_ms

    @classmethod
    def count_tokens(cls, text: str) -> int:
        """
        Estimate token count for text.

        This is a rough approximation. For accurate counts,
        use the tokenizer directly.

        Args:
            text: The text to count

        Returns:
            Estimated token count
        """
        # Rough estimate: ~1.5 tokens per word for mixed Hindi/English
        words = text.split()
        return int(len(words) * 1.5)

    @classmethod
    def is_available(cls) -> bool:
        """Check if Gemini service is available."""
        try:
            api_key = getattr(settings, 'GOOGLE_GEMINI_API_KEY', None)
            return bool(api_key)
        except Exception:
            return False
