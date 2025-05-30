from typing import Optional, Union
import asyncio
import logging
import openai
from openai import AsyncOpenAI, OpenAIError
from config import get_settings
from collections.abc import AsyncGenerator
from openai.types.chat import ChatCompletionChunk

from exceptions import LLMServiceException

logger = logging.getLogger(__name__)


class BaseLlmService:
    """Base service for interacting with OpenAI's chat models asynchronously."""

    def __init__(self):
        """Initialize the OpenAI client with configuration settings."""
        self.settings = get_settings()
        self.client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        self.model = self.settings.openai_model
        self.max_retries = self.settings.openai_max_retries
        self.retry_delay = self.settings.openai_retry_delay

    async def _retry_with_backoff(self, func, *args, **kwargs):
        """Retry a coroutine with exponential backoff on transient errors."""
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except (OpenAIError, TimeoutError, ConnectionError) as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (2**attempt))
                else:
                    logger.error(f"Max retries exceeded: {e}")
                    raise LLMServiceException(detail=str(e))

    async def chat_complete(
        self,
        prompt: Optional[str] = None,
        messages: Optional[list[dict]] = None,
        max_tokens: int = 300,
        temperature: float = 0.1,
        top_p: Optional[float] = 1.0,
        stream: bool = False,
    ) -> Union[str, AsyncGenerator[ChatCompletionChunk, None]]:
        """Send a chat completion request to the OpenAI API with optional streaming."""

        if messages is None:
            messages = [{"role": "user", "content": prompt}]

        async def call_openai():
            return await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stream=stream,
            )

        response = await self._retry_with_backoff(call_openai)
        return response if stream else response.choices[0].message.content
