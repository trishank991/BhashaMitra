"""Google Gemini AI Service for Peppi chatbot using new google-genai SDK."""
import logging
import time
import traceback
from typing import AsyncGenerator

from django.conf import settings

logger = logging.getLogger(__name__)


class GeminiAIService:
    """
    Service for Google Gemini AI integration.

    Uses the new google-genai SDK (replaces deprecated google-generativeai).

    Handles:
    - API communication with Gemini
    - Message history management
    - Streaming responses
    - Token counting and cost tracking
    """

    # Get model settings from Django settings with defaults
    @classmethod
    def get_model_id(cls):
        # gemini-2.0-flash is the recommended model for fast responses
        return getattr(settings, 'GEMINI_MODEL_ID', 'gemini-2.0-flash')

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
        Get or create the Gemini client using the new google-genai SDK.

        Returns:
            genai.Client: The Gemini client instance
        """
        if cls._client is None:
            try:
                from google import genai

                api_key = getattr(settings, 'GOOGLE_GEMINI_API_KEY', None)
                if not api_key:
                    logger.error("GOOGLE_GEMINI_API_KEY is not set in settings")
                    raise ValueError("GOOGLE_GEMINI_API_KEY not configured")

                logger.info(f"Configuring Gemini with API key (first 8 chars): {api_key[:8]}...")

                # Create client with API key
                cls._client = genai.Client(api_key=api_key)

                model_id = cls.get_model_id()
                logger.info(f"Gemini client initialized, will use model: {model_id}")

            except ImportError:
                logger.error("google-genai package not installed")
                raise ImportError("Please install google-genai: pip install google-genai")

        return cls._client

    @classmethod
    def build_conversation_contents(
        cls,
        conversation,
        user_message: str,
        system_prompt: str,
        max_messages: int = 20,
    ) -> list:
        """
        Build conversation contents for the API call.

        The new SDK uses a different format - we build a list of Content objects.

        Args:
            conversation: PeppiConversation instance
            user_message: The current user message
            system_prompt: The system prompt to include
            max_messages: Maximum number of history messages to include

        Returns:
            List of content parts for the API
        """
        from google.genai import types
        from apps.peppi_chat.models import PeppiChatMessage

        contents = []

        # Add system prompt as first user message with model acknowledgment
        contents.append(types.Content(
            role="user",
            parts=[types.Part.from_text(text=system_prompt)]
        ))
        contents.append(types.Content(
            role="model",
            parts=[types.Part.from_text(text="I understand! I am Peppi, and I will follow these instructions carefully. Ready to help!")]
        ))

        # Get conversation history
        messages = PeppiChatMessage.objects.filter(
            conversation=conversation
        ).order_by('-created_at')[:max_messages]

        # Reverse to get chronological order
        messages = list(reversed(messages))

        for msg in messages:
            role = "user" if msg.role == 'user' else "model"
            contents.append(types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg.content_primary)]
            ))

        # Add the current user message
        contents.append(types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_message)]
        ))

        return contents

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
        Generate a response from Gemini (async version).

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
            from google.genai import types

            client = cls.get_client()
            model_id = cls.get_model_id()

            # Build conversation contents
            contents = cls.build_conversation_contents(
                conversation,
                user_message,
                system_prompt
            )

            # Configure generation settings
            config = types.GenerateContentConfig(
                temperature=cls.get_temperature(),
                top_p=cls.TOP_P,
                top_k=cls.TOP_K,
                max_output_tokens=cls.get_max_tokens(),
                safety_settings=[
                    types.SafetySetting(
                        category='HARM_CATEGORY_HARASSMENT',
                        threshold='BLOCK_MEDIUM_AND_ABOVE'
                    ),
                    types.SafetySetting(
                        category='HARM_CATEGORY_HATE_SPEECH',
                        threshold='BLOCK_MEDIUM_AND_ABOVE'
                    ),
                    types.SafetySetting(
                        category='HARM_CATEGORY_SEXUALLY_EXPLICIT',
                        threshold='BLOCK_LOW_AND_ABOVE'
                    ),
                    types.SafetySetting(
                        category='HARM_CATEGORY_DANGEROUS_CONTENT',
                        threshold='BLOCK_MEDIUM_AND_ABOVE'
                    ),
                ],
            )

            if stream:
                # Streaming response
                response = await client.aio.models.generate_content_stream(
                    model=model_id,
                    contents=contents,
                    config=config,
                )

                full_text = ""
                async for chunk in response:
                    if chunk.text:
                        full_text += chunk.text
                        yield chunk.text

                latency_ms = int((time.time() - start_time) * 1000)
                logger.info(
                    f"Gemini streaming response completed: "
                    f"{len(full_text)} chars, {latency_ms}ms"
                )
            else:
                # Non-streaming response
                response = await client.aio.models.generate_content(
                    model=model_id,
                    contents=contents,
                    config=config,
                )

                latency_ms = int((time.time() - start_time) * 1000)
                logger.info(
                    f"Gemini response: {len(response.text)} chars, {latency_ms}ms"
                )

                yield response.text

        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
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
            from google.genai import types

            client = cls.get_client()
            model_id = cls.get_model_id()

            # Build conversation contents
            contents = cls.build_conversation_contents(
                conversation,
                user_message,
                system_prompt
            )

            # Configure generation settings
            config = types.GenerateContentConfig(
                temperature=cls.get_temperature(),
                top_p=cls.TOP_P,
                top_k=cls.TOP_K,
                max_output_tokens=cls.get_max_tokens(),
                safety_settings=[
                    types.SafetySetting(
                        category='HARM_CATEGORY_HARASSMENT',
                        threshold='BLOCK_MEDIUM_AND_ABOVE'
                    ),
                    types.SafetySetting(
                        category='HARM_CATEGORY_HATE_SPEECH',
                        threshold='BLOCK_MEDIUM_AND_ABOVE'
                    ),
                    types.SafetySetting(
                        category='HARM_CATEGORY_SEXUALLY_EXPLICIT',
                        threshold='BLOCK_LOW_AND_ABOVE'
                    ),
                    types.SafetySetting(
                        category='HARM_CATEGORY_DANGEROUS_CONTENT',
                        threshold='BLOCK_MEDIUM_AND_ABOVE'
                    ),
                ],
            )

            # Generate response
            response = client.models.generate_content(
                model=model_id,
                contents=contents,
                config=config,
            )

            latency_ms = int((time.time() - start_time) * 1000)

            # Get response text
            response_text = response.text

            # Estimate token count (rough approximation)
            token_count = len(response_text.split()) * 2

            logger.info(
                f"Gemini sync response: {len(response_text)} chars, "
                f"~{token_count} tokens, {latency_ms}ms"
            )

            return response_text, token_count, latency_ms

        except Exception as e:
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
