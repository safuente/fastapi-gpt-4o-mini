import pytest
from schemas.analyze import AnalysisType
from schemas import AnalysisResponse


@pytest.mark.asyncio
async def test_sentiment_analysis(analysis_service, mock_chat):
    mock_chat(analysis_service, "Sentiment: Positive\nConfidence: 95%")

    response = await analysis_service.analyze_text("Positive text sample", AnalysisType.SENTIMENT)

    assert isinstance(response, AnalysisResponse)
    assert "Positive" in response.result
