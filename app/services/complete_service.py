import uuid
import logging
from schemas import CompletionResponse
from openai.types.chat import ChatCompletionChunk
from fastapi.responses import StreamingResponse
from typing import Union, AsyncGenerator
from services.base_llm_service import BaseLlmService

logger = logging.getLogger(__name__)


class CompletionService(BaseLlmService):

    async def chat_completion(
        self,
        prompt: str,
        max_tokens: int = 150,
        temperature: float = 0.7,
        top_p: float = 1.0,
        system_prompt: str = "You complete the user's text without explanations, in a natural and continuous way.",
        stream: bool = False,
    ) -> Union[CompletionResponse, AsyncGenerator[ChatCompletionChunk, None]]:

        logger.info("Starting text completion...")
        logger.debug(f"Prompt: {prompt}")
        logger.debug(f"System prompt: {system_prompt}")
        logger.debug(
            f"Parameters - max_tokens: {max_tokens}, temperature: {temperature}, top_p: {top_p}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        completion = await self.chat_complete(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=stream,
        )
        if stream:
            logger.info("Using streaming in chat completion")

            async def text_stream():
                async for chunk in completion:
                    if chunk.choices and chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content

            return StreamingResponse(text_stream(), media_type="text/plain")

        logger.info(f"Completion generated successfully")

        return CompletionResponse(completion=completion.strip())
