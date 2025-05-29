from typing import Optional, Union
import asyncio
import logging
import openai
from openai import AsyncOpenAI
from config import get_settings
from collections.abc import AsyncGenerator
from openai.types.chat import ChatCompletionChunk

logger = logging.getLogger(__name__)


class BaseLlmService:
    def __init__(self):
        self.settings = get_settings()
        self.client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        self.model = "gpt-4o-mini"
        self.max_retries = 3
        self.retry_delay = 1.0

    async def chat_complete(
        self,
        prompt: str,
        max_tokens: int = 300,
        temperature: float = 0.1,
        top_p: Optional[float] = 1.0,
        stream: bool = False,
    ) -> Union[str, AsyncGenerator[ChatCompletionChunk, None]]:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=stream,
        )
        return response if stream else response.choices[0].message.content
