from services.base_llm_service import BaseLlmService
from schemas import SummaryResponse
from logger import logger


class SummaryService(BaseLlmService):
    """Service to handle summarization prompts"""

    def __init__(self):
        super().__init__()

    async def summarize_text(
        self, text: str, max_length: int = 150, style: str = "concise"
    ) -> SummaryResponse:
        logger.info(
            f"Starting summarization with style='{style}' and max_length={max_length}"
        )

        style_prompts = {
            "concise": "Provide a concise summary:",
            "detailed": "Provide a detailed summary:",
            "bullet_points": "Summarize using bullet points:",
            "executive": "Provide an executive summary:",
            "storytelling": "Summarize in a narrative storytelling style:",
        }

        prompt = (
            f"{style_prompts.get(style, style_prompts['concise'])}\n\n"
            f"Text: {text}\n\n"
            f"Summary (max {max_length} words):"
        )

        logger.debug(f"Generated prompt for model:\n{prompt}")

        try:
            summary: str = await self.chat_complete(
                prompt=prompt, max_tokens=min(max_length * 2, 500), temperature=0.3
            )
        except Exception as e:
            logger.exception("Error during chat completion")
            raise

        result = SummaryResponse(
            summary=summary.strip(),
            original_length=len(text.split()),
            summary_length=len(summary.split()),
        )

        logger.info(
            f"Generated summary ({result.summary_length} words from {result.original_length})"
        )

        return result
