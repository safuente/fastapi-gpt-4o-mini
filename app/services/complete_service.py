import logging
from schemas import CompletionResponse
from openai.types.chat import ChatCompletionChunk
from typing import Union, AsyncGenerator
from services.base_llm_service import BaseLlmService

logger = logging.getLogger(__name__)


class CompletionService(BaseLlmService):
    """Service for generating text completions using a chat-based LLM."""

    async def chat_completion(
        self,
        prompt: str,
        max_tokens: int = 150,
        temperature: float = 0.7,
        top_p: float = 1.0,
        system_prompt: str = "You complete the user's text without explanations, in a natural and continuous way.",
        stream: bool = False,
    ) -> Union[CompletionResponse, AsyncGenerator[ChatCompletionChunk, None]]:
        """
        Generate a text completion, either as full response or streaming generator.
        """
        logger.info("Starting text completion...")
        logger.debug(f"Prompt: {prompt}")
        logger.debug(f"System prompt: {system_prompt}")
        logger.debug(
            f"Parameters - max_tokens: {max_tokens}, temperature: {temperature}, top_p: {top_p}, stream: {stream}"
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
            logger.info("Returning async generator for streaming")
            return completion

        logger.info("Completion generated successfully")
        return CompletionResponse(completion=completion.strip())
