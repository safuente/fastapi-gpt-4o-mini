import pytest
from schemas import SummaryResponse


@pytest.mark.asyncio
async def test_summarize_text_returns_response(summary_service, mock_chat):
    mock_chat(summary_service, "Simulated summary of the original text.")

    input_text = "This is a sample input text that should be summarized by the model."
    result = await summary_service.summarize_text(
        text=input_text, max_length=50, style="concise"
    )

    assert isinstance(result, SummaryResponse)
    assert "Simulated" in result.summary
    assert result.original_length == len(input_text.split())
    assert result.summary_length == len(result.summary.split())
