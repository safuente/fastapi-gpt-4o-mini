from services.base_llm_service import BaseLlmService
from schemas.analyze import AnalysisType
import logging

from exceptions import AppException

from schemas import AnalysisResponse

logger = logging.getLogger(__name__)


class AnalysisService(BaseLlmService):
    """
    Service for performing various types of text analysis using an LLM.
    """

    async def analyze_text(
        self, text: str, analysis_type: AnalysisType
    ) -> AnalysisResponse:
        """
        Analyze the given text using the specified type of analysis.
        """
        analysis_prompts = {
            AnalysisType.SENTIMENT: "Analyze the sentiment of this text (positive, negative, neutral) and provide a confidence score:",
            AnalysisType.KEY_TOPICS: "Extract the key topics and themes from this text:",
            AnalysisType.ENTITIES: "Identify named entities (people, places, organizations) in this text:",
            AnalysisType.READABILITY: "Assess the readability level of this text:",
            AnalysisType.TONE: "Analyze the tone and writing style of this text:",
        }

        prompt_template = analysis_prompts.get(analysis_type)

        if not prompt_template:
            supported = ", ".join([t.value for t in AnalysisType])
            raise AppException(
                message=f"Unsupported analysis type: '{analysis_type}'. Supported types are: {supported}",
                error_code="unsupported_analysis_type",
            )

        full_prompt = (
            f"{prompt_template}\n\n"
            f"Return your response in the same language as the input text.\n\n"
            f"Text:\n{text}"
        )

        logger.info(f"Performing analysis: {analysis_type}")
        logger.debug(f"Prompt:\n{full_prompt}")

        messages = [
            {"role": "system", "content": "You are an expert text analyst."},
            {"role": "user", "content": full_prompt},
        ]

        result = await self.chat_complete(
            messages=messages, max_tokens=400, temperature=0.3, top_p=1.0, stream=False
        )
        logger.info(result)

        return AnalysisResponse(result=result.strip())
