# services/translation_service.py

from services.base_llm_service import BaseLlmService
from schemas.translate import TranslationResponse
import logging

logger = logging.getLogger(__name__)


class TranslationService(BaseLlmService):
    async def translate_text(self, text: str, target_language: str) -> TranslationResponse:
        logger.info(f"Translating to '{target_language}'")

        prompt = (
            f"Translate the following text to {target_language.upper()}:\n\n"
            f"{text}"
        )

        messages = [
            {"role": "system", "content": "You are a professional translator."},
            {"role": "user", "content": prompt}
        ]

        completion = await self.chat_complete(
            messages=messages,
            max_tokens=300,
            temperature=0.3,
            top_p=1.0,
            stream=False
        )

        return TranslationResponse(translation=completion.strip())
